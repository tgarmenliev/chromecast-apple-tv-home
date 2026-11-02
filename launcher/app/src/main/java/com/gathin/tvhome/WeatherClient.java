package com.gathin.tvhome;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Handler;
import android.os.Looper;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.Locale;

/**
 * Weather for one place from Open-Meteo (no key): now, today's range and the next days. The place is
 * config.xml weather_lat / weather_lon (with weather_city as the label); with no coordinates the city name is
 * looked up once. One request at most every 30 minutes, only while Home is on screen; the last answer is cached
 * and shown at once.
 */
final class WeatherClient {

    interface Listener {
        void onWeather(JSONObject forecast, String place);
    }

    private static final long MAX_AGE_MS = 30 * 60 * 1000L;
    private static final int TIMEOUT_MS = 8000;

    private final Context ctx;
    private final SharedPreferences prefs;
    private final Handler main = new Handler(Looper.getMainLooper());
    private boolean busy;

    WeatherClient(Context ctx) {
        this.ctx = ctx.getApplicationContext();
        this.prefs = this.ctx.getSharedPreferences("weather2", Context.MODE_PRIVATE);
    }

    private String city() {
        return ctx.getString(R.string.weather_city).trim();
    }

    private String lat() {
        return ctx.getString(R.string.weather_lat).trim();
    }

    private String lon() {
        return ctx.getString(R.string.weather_lon).trim();
    }

    void load(Listener listener) {
        final String city = city();
        if (city.isEmpty() && lat().isEmpty()) return;
        final String key = city + "|" + lat() + "|" + lon();
        String cached = prefs.getString("json", "");
        boolean same = key.equals(prefs.getString("key", ""));
        if (same && !cached.isEmpty()) {
            try {
                listener.onWeather(new JSONObject(cached), city);
            } catch (Exception ignored) {
            }
        }
        if (busy || (same && System.currentTimeMillis() - prefs.getLong("at", 0) < MAX_AGE_MS)) return;
        busy = true;
        new Thread(() -> {
            try {
                double la, lo;
                if (!lat().isEmpty() && !lon().isEmpty()) {
                    la = Double.parseDouble(lat());
                    lo = Double.parseDouble(lon());
                } else {
                    JSONObject geo = get("https://geocoding-api.open-meteo.com/v1/search?count=1&language=en&format=json&name="
                            + URLEncoder.encode(city, "UTF-8"));
                    JSONArray found = geo.optJSONArray("results");
                    if (found == null || found.length() == 0) throw new IllegalStateException("unknown city");
                    la = found.getJSONObject(0).getDouble("latitude");
                    lo = found.getJSONObject(0).getDouble("longitude");
                }
                JSONObject w = get(String.format(Locale.US,
                        "https://api.open-meteo.com/v1/forecast?latitude=%.4f&longitude=%.4f"
                                + "&current=temperature_2m,apparent_temperature,weather_code,is_day,wind_speed_10m,relative_humidity_2m"
                                + "&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset"
                                + "&timezone=auto&forecast_days=5&wind_speed_unit=kmh", la, lo));
                prefs.edit().putString("key", key).putString("json", w.toString())
                        .putLong("at", System.currentTimeMillis()).apply();
                main.post(() -> listener.onWeather(w, city));
            } catch (Exception ignored) {
                // Offline or the service is down: whatever was cached stays on screen.
            } finally {
                busy = false;
            }
        }, "weather").start();
    }

    private static JSONObject get(String url) throws Exception {
        HttpURLConnection c = (HttpURLConnection) new URL(url).openConnection();
        c.setConnectTimeout(TIMEOUT_MS);
        c.setReadTimeout(TIMEOUT_MS);
        try (BufferedReader r = new BufferedReader(new InputStreamReader(c.getInputStream(), StandardCharsets.UTF_8))) {
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = r.readLine()) != null) sb.append(line);
            return new JSONObject(sb.toString());
        } finally {
            c.disconnect();
        }
    }
}
