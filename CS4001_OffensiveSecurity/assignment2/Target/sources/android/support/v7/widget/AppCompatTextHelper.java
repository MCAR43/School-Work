package android.support.v7.widget;

import android.content.Context;
import android.content.res.ColorStateList;
import android.content.res.TypedArray;
import android.os.Build;
import android.support.v7.appcompat.R;
import android.support.v7.internal.text.AllCapsTransformationMethod;
import android.support.v7.internal.widget.ThemeUtils;
import android.util.AttributeSet;
import android.widget.TextView;

class AppCompatTextHelper {
    private static final int[] TEXT_APPEARANCE_ATTRS = {R.attr.textAllCaps};
    private static final int[] VIEW_ATTRS = {16842804};
    private final TextView mView;

    AppCompatTextHelper(TextView view) {
        this.mView = view;
    }

    /* access modifiers changed from: package-private */
    public void loadFromAttributes(AttributeSet attrs, int defStyleAttr) {
        int disabledTextColor;
        Context context = this.mView.getContext();
        TypedArray a = context.obtainStyledAttributes(attrs, VIEW_ATTRS, defStyleAttr, 0);
        int ap = a.getResourceId(0, -1);
        a.recycle();
        if (ap != -1) {
            TypedArray appearance = context.obtainStyledAttributes(ap, R.styleable.TextAppearance);
            if (appearance.hasValue(R.styleable.TextAppearance_textAllCaps)) {
                setAllCaps(appearance.getBoolean(R.styleable.TextAppearance_textAllCaps, false));
            }
            appearance.recycle();
        }
        TypedArray a2 = context.obtainStyledAttributes(attrs, TEXT_APPEARANCE_ATTRS, defStyleAttr, 0);
        if (a2.hasValue(0)) {
            setAllCaps(a2.getBoolean(0, false));
        }
        a2.recycle();
        ColorStateList textColors = this.mView.getTextColors();
        if (textColors != null && !textColors.isStateful()) {
            if (Build.VERSION.SDK_INT < 21) {
                disabledTextColor = ThemeUtils.getDisabledThemeAttrColor(context, 16842808);
            } else {
                disabledTextColor = ThemeUtils.getThemeAttrColor(context, 16842808);
            }
            this.mView.setTextColor(ThemeUtils.createDisabledStateList(textColors.getDefaultColor(), disabledTextColor));
        }
    }

    /* access modifiers changed from: package-private */
    public void onSetTextAppearance(Context context, int resId) {
        TypedArray appearance = context.obtainStyledAttributes(resId, TEXT_APPEARANCE_ATTRS);
        if (appearance.hasValue(0)) {
            setAllCaps(appearance.getBoolean(0, false));
        }
        appearance.recycle();
    }

    /* access modifiers changed from: package-private */
    public void setAllCaps(boolean allCaps) {
        this.mView.setTransformationMethod(allCaps ? new AllCapsTransformationMethod(this.mView.getContext()) : null);
    }
}
