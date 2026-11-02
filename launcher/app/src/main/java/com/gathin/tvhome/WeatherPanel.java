package com.gathin.tvhome;

import android.content.Context;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.util.TypedValue;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONObject;

import java.time.LocalDate;
import java.time.format.TextStyle;
import java.util.Locale;

/**
 * The weather card on Home: a glass panel on the right with the current temperature and symbol, the day's range,
 * wind, chance of rain and sunset, and the next four days. Built in code and filled from one Open-Meteo answer
 * (WeatherClient); it never takes focus.
 */
final class WeatherPanel extends LinearLayout {

    private final Typeface light, regular, medium;
    private final float dp;
    /** The blurred wallpaper under the card; set by MainActivity, resized and shown with the card. */
    private WeatherBackdrop backdrop;

    WeatherPanel(Context context) {
        super(context);
        dp = context.getResources().getDisplayMetrics().density;
        light = UiFont.get(context, R.string.font_light);
        regular = UiFont.get(context, R.string.font_regular);
        medium = UiFont.get(context, R.string.font_medium);
        setOrientation(VERTICAL);
        setFocusable(false);
        setImportantForAccessibility(IMPORTANT_FOR_ACCESSIBILITY_NO);
        GradientDrawable bg = new GradientDrawable();
        bg.setColor(0x66080C14);
        bg.setCornerRadius(px(22));
        bg.setStroke(Math.max(1, px(1)), 0x2EFFFFFF);
        setBackground(bg);
        setPadding(px(20), px(12), px(20), px(12));
        setVisibility(GONE);
    }

    void setBackdrop(WeatherBackdrop view) {
        backdrop = view;
    }

    @Override
    protected void onLayout(boolean changed, int l, int t, int r, int b) {
        super.onLayout(changed, l, t, r, b);
        if (backdrop != null) {
            ViewGroup.LayoutParams lp = backdrop.getLayoutParams();
            if (lp.width != r - l || lp.height != b - t) {
                lp.width = r - l;
                lp.height = b - t;
                backdrop.setLayoutParams(lp);
            }
        }
    }

    @Override
    public void setVisibility(int visibility) {
        super.setVisibility(visibility);
        if (backdrop != null) backdrop.setVisibility(visibility);
    }

    private int px(float v) {
        return Math.round(v * dp);
    }

    private TextView text(String s, float sp, Typeface face, int color, float spacing) {
        TextView t = new TextView(getContext());
        t.setText(s);
        t.setTextSize(TypedValue.COMPLEX_UNIT_SP, sp);
        t.setTypeface(face);
        t.setTextColor(color);
        t.setLetterSpacing(spacing);
        t.setSingleLine(true);
        t.setIncludeFontPadding(false);
        return t;
    }

    void bind(JSONObject w, String place) {
        try {
            JSONObject cur = w.getJSONObject("current");
            JSONObject day = w.getJSONObject("daily");
            JSONArray dates = day.getJSONArray("time");
            JSONArray codes = day.getJSONArray("weather_code");
            JSONArray hi = day.getJSONArray("temperature_2m_max");
            JSONArray lo = day.getJSONArray("temperature_2m_min");
            JSONArray rain = day.optJSONArray("precipitation_probability_max");
            JSONArray sunset = day.optJSONArray("sunset");
            int code = cur.getInt("weather_code");
            boolean isDay = cur.optInt("is_day", 1) == 1;

            removeAllViews();

            // Top: symbol, big temperature, description and place.
            LinearLayout top = new LinearLayout(getContext());
            top.setOrientation(HORIZONTAL);
            top.setGravity(Gravity.CENTER_VERTICAL);
            WeatherIconView icon = new WeatherIconView(getContext());
            icon.set(code, isDay);
            top.addView(icon, new LayoutParams(px(54), px(54)));

            TextView temp = text(Math.round(cur.getDouble("temperature_2m")) + "°", 52, light, 0xFFFFFFFF, -0.03f);
            LayoutParams tp = new LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT);
            tp.setMarginStart(px(12));
            top.addView(temp, tp);

            LinearLayout info = new LinearLayout(getContext());
            info.setOrientation(VERTICAL);
            info.addView(text(WeatherIconView.describe(code), 17, medium, 0xFFFFFFFF, 0.01f));
            String feels = "Feels " + Math.round(cur.getDouble("apparent_temperature")) + "°  ·  H "
                    + Math.round(hi.getDouble(0)) + "°  L " + Math.round(lo.getDouble(0)) + "°";
            TextView f = text(feels, 13, regular, 0xB3FFFFFF, 0.03f);
            LayoutParams fp = new LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT);
            fp.topMargin = px(2);
            info.addView(f, fp);
            if (!place.isEmpty()) {
                TextView p = text(place.toUpperCase(Locale.ENGLISH), 11, medium, 0x8CFFFFFF, 0.22f);
                LayoutParams pp = new LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT);
                pp.topMargin = px(4);
                info.addView(p, pp);
            }
            LayoutParams ip = new LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT);
            ip.setMarginStart(px(16));
            top.addView(info, ip);
            addView(top);

            // Wind, rain chance and sunset in one quiet line.
            StringBuilder line = new StringBuilder();
            line.append("WIND ").append(Math.round(cur.optDouble("wind_speed_10m", 0))).append(" KM/H");
            if (rain != null && rain.length() > 0 && !rain.isNull(0)) {
                line.append("   ·   RAIN ").append(rain.getInt(0)).append("%");
            }
            if (sunset != null && sunset.length() > 0) {
                String s = sunset.getString(0);
                int t = s.indexOf('T');
                if (t > 0) line.append("   ·   SUNSET ").append(s.substring(t + 1));
            }
            TextView meta = text(line.toString(), 11, medium, 0x99FFFFFF, 0.14f);
            LayoutParams mp = new LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT);
            mp.topMargin = px(8);
            addView(meta, mp);

            View rule = new View(getContext());
            rule.setBackgroundColor(0x24FFFFFF);
            LayoutParams rp = new LayoutParams(LayoutParams.MATCH_PARENT, Math.max(1, px(1)));
            rp.topMargin = px(8);
            addView(rule, rp);

            // The next four days.
            LinearLayout days = new LinearLayout(getContext());
            days.setOrientation(HORIZONTAL);
            for (int i = 1; i < dates.length() && i <= 4; i++) {
                LinearLayout col = new LinearLayout(getContext());
                col.setOrientation(VERTICAL);
                col.setGravity(Gravity.CENTER_HORIZONTAL);
                String name = LocalDate.parse(dates.getString(i)).getDayOfWeek()
                        .getDisplayName(TextStyle.SHORT, Locale.ENGLISH).toUpperCase(Locale.ENGLISH);
                col.addView(text(name, 11, medium, 0xB3FFFFFF, 0.2f), new LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT));
                WeatherIconView di = new WeatherIconView(getContext());
                di.set(codes.getInt(i), true);
                LayoutParams dip = new LayoutParams(px(26), px(26));
                dip.topMargin = px(4);
                col.addView(di, dip);
                TextView h = text(Math.round(hi.getDouble(i)) + "°", 16, regular, 0xFFFFFFFF, 0f);
                LayoutParams hp = new LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT);
                hp.topMargin = px(4);
                col.addView(h, hp);
                col.addView(text(Math.round(lo.getDouble(i)) + "°", 13, regular, 0x80FFFFFF, 0f), new LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT));
                LayoutParams cp = new LayoutParams(px(76), LayoutParams.WRAP_CONTENT);
                days.addView(col, cp);
            }
            LayoutParams dp2 = new LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT);
            dp2.topMargin = px(8);
            addView(days, dp2);
            setVisibility(VISIBLE);
        } catch (Exception e) {
            // A malformed answer leaves whatever was shown before.
        }
    }
}
