package com.gathin.tvhome;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Matrix;
import android.graphics.Outline;
import android.graphics.Paint;
import android.graphics.RenderEffect;
import android.graphics.Shader;
import android.os.Build;
import android.view.View;
import android.view.ViewOutlineProvider;

/**
 * Frosted glass under the weather card: the part of the wallpaper behind the card, blurred. It sits in Home's root
 * just under the card and takes the card's size (WeatherPanel keeps them equal); the picture is drawn exactly where
 * the wallpaper is, so the blur lines up with what it hides.
 */
final class WeatherBackdrop extends View {

    private final Paint paint = new Paint(Paint.FILTER_BITMAP_FLAG);
    private final Matrix matrix = new Matrix();
    private Bitmap bitmap;
    private int screenWidth, screenHeight;

    WeatherBackdrop(Context context) {
        super(context);
        final float radius = 22 * context.getResources().getDisplayMetrics().density;
        setImportantForAccessibility(IMPORTANT_FOR_ACCESSIBILITY_NO);
        setFocusable(false);
        setOutlineProvider(new ViewOutlineProvider() {
            @Override
            public void getOutline(View view, Outline outline) {
                outline.setRoundRect(0, 0, view.getWidth(), view.getHeight(), radius);
            }
        });
        setClipToOutline(true);
        if (Build.VERSION.SDK_INT >= 31) {
            setRenderEffect(RenderEffect.createBlurEffect(26f, 26f, Shader.TileMode.CLAMP));
        }
        setVisibility(GONE);
    }

    /** The wallpaper now on screen, and the screen size it is centre-cropped to. */
    void setWallpaper(Bitmap picture, int width, int height) {
        bitmap = picture;
        screenWidth = width;
        screenHeight = height;
        invalidate();
    }

    @Override
    protected void onDraw(Canvas canvas) {
        Bitmap b = bitmap;
        if (b == null || b.isRecycled() || screenWidth <= 0) return;
        float scale = Math.max(screenWidth / (float) b.getWidth(), screenHeight / (float) b.getHeight());
        float dx = (screenWidth - b.getWidth() * scale) / 2f - getLeft();
        float dy = (screenHeight - b.getHeight() * scale) / 2f - getTop();
        matrix.setScale(scale, scale);
        matrix.postTranslate(dx, dy);
        canvas.drawBitmap(b, matrix, paint);
    }
}
