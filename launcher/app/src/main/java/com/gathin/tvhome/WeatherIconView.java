package com.gathin.tvhome;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.RectF;
import android.view.View;

/** One weather symbol drawn in code (no image files, no emoji font): sun, moon, clouds, rain, snow, storm, fog. */
final class WeatherIconView extends View {

    static final int CLEAR = 0, PARTLY = 1, CLOUDY = 2, FOG = 3, RAIN = 4, SNOW = 5, STORM = 6;

    private static final int SUN = 0xFFFFC857, MOON = 0xFFE9EEF9, CLOUD = 0xFFEAF0F8, CLOUD_DARK = 0xFFB9C4D6,
            DROP = 0xFF74B9FF, BOLT = 0xFFFFD95A;

    private final Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final Path path = new Path();
    private final RectF rect = new RectF();
    private int kind = CLOUDY;
    private boolean day = true;

    WeatherIconView(Context context) {
        super(context);
        setImportantForAccessibility(IMPORTANT_FOR_ACCESSIBILITY_NO);
    }

    /** WMO weather code to one of the kinds above. */
    static int kindOf(int code) {
        if (code == 0) return CLEAR;
        if (code <= 2) return PARTLY;
        if (code == 3) return CLOUDY;
        if (code == 45 || code == 48) return FOG;
        if ((code >= 51 && code <= 67) || (code >= 80 && code <= 82)) return RAIN;
        if ((code >= 71 && code <= 77) || code == 85 || code == 86) return SNOW;
        if (code >= 95) return STORM;
        return CLOUDY;
    }

    static String describe(int code) {
        if (code == 0) return "Clear sky";
        if (code == 1) return "Mostly clear";
        if (code == 2) return "Partly cloudy";
        if (code == 3) return "Overcast";
        if (code == 45 || code == 48) return "Fog";
        if (code >= 51 && code <= 57) return "Drizzle";
        if (code >= 61 && code <= 65) return "Rain";
        if (code == 66 || code == 67) return "Freezing rain";
        if (code >= 71 && code <= 75) return "Snow";
        if (code == 77) return "Snow grains";
        if (code >= 80 && code <= 82) return "Rain showers";
        if (code == 85 || code == 86) return "Snow showers";
        if (code >= 95) return "Thunderstorm";
        return "Cloudy";
    }

    void set(int code, boolean isDay) {
        kind = kindOf(code);
        day = isDay;
        invalidate();
    }

    @Override
    protected void onDraw(Canvas c) {
        float s = Math.min(getWidth(), getHeight());
        if (s <= 0) return;
        c.save();
        c.translate((getWidth() - s) / 2f, (getHeight() - s) / 2f);
        c.scale(s / 100f, s / 100f);
        switch (kind) {
            case CLEAR:
                body(c, 50, 50, 1f);
                break;
            case PARTLY:
                body(c, 36, 36, 0.72f);
                cloud(c, 8, 38, 1f, CLOUD);
                break;
            case CLOUDY:
                cloud(c, 20, 6, 0.8f, CLOUD_DARK);
                cloud(c, 4, 26, 1f, CLOUD);
                break;
            case FOG:
                cloud(c, 4, 4, 1f, CLOUD);
                paint.setStyle(Paint.Style.STROKE);
                paint.setStrokeCap(Paint.Cap.ROUND);
                paint.setStrokeWidth(5f);
                paint.setColor(CLOUD_DARK);
                c.drawLine(18, 66, 82, 66, paint);
                c.drawLine(28, 78, 90, 78, paint);
                c.drawLine(14, 90, 70, 90, paint);
                break;
            case RAIN:
                cloud(c, 4, 0, 1f, CLOUD_DARK);
                paint.setStyle(Paint.Style.STROKE);
                paint.setStrokeCap(Paint.Cap.ROUND);
                paint.setStrokeWidth(5.5f);
                paint.setColor(DROP);
                c.drawLine(30, 66, 24, 82, paint);
                c.drawLine(50, 66, 44, 82, paint);
                c.drawLine(70, 66, 64, 82, paint);
                c.drawLine(40, 80, 36, 92, paint);
                c.drawLine(60, 80, 56, 92, paint);
                break;
            case SNOW:
                cloud(c, 4, 0, 1f, CLOUD_DARK);
                paint.setStyle(Paint.Style.FILL);
                paint.setColor(0xFFFFFFFF);
                for (int i = 0; i < 3; i++) c.drawCircle(30 + i * 20, 72, 4.2f, paint);
                for (int i = 0; i < 2; i++) c.drawCircle(40 + i * 20, 87, 4.2f, paint);
                break;
            default:
                cloud(c, 4, 0, 1f, 0xFF8E9BB3);
                paint.setStyle(Paint.Style.FILL);
                paint.setColor(BOLT);
                path.reset();
                path.moveTo(54, 56);
                path.lineTo(36, 80);
                path.lineTo(48, 80);
                path.lineTo(42, 98);
                path.lineTo(66, 70);
                path.lineTo(53, 70);
                path.lineTo(60, 56);
                path.close();
                c.drawPath(path, paint);
                break;
        }
        c.restore();
    }

    /** The sun by day (disc and rays), a crescent moon by night, centred at (cx, cy) in the 100 unit box. */
    private void body(Canvas c, float cx, float cy, float scale) {
        if (day) {
            paint.setStyle(Paint.Style.FILL);
            paint.setColor(SUN);
            c.drawCircle(cx, cy, 17f * scale, paint);
            paint.setStyle(Paint.Style.STROKE);
            paint.setStrokeCap(Paint.Cap.ROUND);
            paint.setStrokeWidth(5f * scale);
            for (int i = 0; i < 8; i++) {
                double a = Math.PI / 4 * i;
                float c0 = (float) Math.cos(a), s0 = (float) Math.sin(a);
                c.drawLine(cx + c0 * 26f * scale, cy + s0 * 26f * scale, cx + c0 * 36f * scale, cy + s0 * 36f * scale, paint);
            }
        } else {
            float r = 24f * scale;
            Path disc = new Path();
            disc.addCircle(cx, cy, r, Path.Direction.CW);
            Path bite = new Path();
            bite.addCircle(cx + r * 0.55f, cy - r * 0.35f, r * 0.85f, Path.Direction.CW);
            path.reset();
            path.op(disc, bite, Path.Op.DIFFERENCE);
            paint.setStyle(Paint.Style.FILL);
            paint.setColor(MOON);
            c.drawPath(path, paint);
        }
    }

    /** A cloud with its top-left corner at (x, y), about 92 wide and 56 tall at scale 1. */
    private void cloud(Canvas c, float x, float y, float scale, int color) {
        paint.setStyle(Paint.Style.FILL);
        paint.setColor(color);
        c.save();
        c.translate(x, y);
        c.scale(scale, scale);
        c.drawCircle(26, 38, 17, paint);
        c.drawCircle(46, 28, 22, paint);
        c.drawCircle(68, 38, 17, paint);
        rect.set(26, 38, 68, 55);
        c.drawRoundRect(rect, 8, 8, paint);
        rect.set(10, 38, 84, 55);
        c.drawRoundRect(rect, 8, 8, paint);
        c.restore();
    }
}
