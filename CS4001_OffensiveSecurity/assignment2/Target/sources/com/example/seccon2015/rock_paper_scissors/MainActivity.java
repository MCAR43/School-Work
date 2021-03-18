package com.example.seccon2015.rock_paper_scissors;

import android.app.Activity;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import java.util.Random;

public class MainActivity extends Activity implements View.OnClickListener {
    Button P;
    Button S;
    int cnt = 0;
    int flag;
    private final Handler handler = new Handler();
    int m;
    int n;
    Button r;
    private final Runnable showMessageTask = new Runnable() {
        public void run() {
            TextView tv3 = (TextView) MainActivity.this.findViewById(R.id.textView3);
            if (MainActivity.this.n - MainActivity.this.m == 1) {
                MainActivity.this.cnt++;
                tv3.setText("WIN! +" + String.valueOf(MainActivity.this.cnt));
            } else if (MainActivity.this.m - MainActivity.this.n == 1) {
                MainActivity.this.cnt = 0;
                tv3.setText("LOSE +0");
            } else if (MainActivity.this.m == MainActivity.this.n) {
                tv3.setText("DRAW +" + String.valueOf(MainActivity.this.cnt));
            } else if (MainActivity.this.m < MainActivity.this.n) {
                MainActivity.this.cnt = 0;
                tv3.setText("LOSE +0");
            } else {
                MainActivity.this.cnt++;
                tv3.setText("WIN! +" + String.valueOf(MainActivity.this.cnt));
            }
            if (959 == MainActivity.this.cnt) {
                tv3.setText("INTEL( " + String.valueOf((MainActivity.this.cnt + MainActivity.this.calc()) * 107) + ")");
            }
            MainActivity.this.flag = 0;
        }
    };

    public native int calc();

    static {
        System.loadLibrary("calc");
    }

    /* access modifiers changed from: protected */
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        this.P = (Button) findViewById(R.id.button);
        this.S = (Button) findViewById(R.id.button3);
        this.r = (Button) findViewById(R.id.buttonR);
        this.P.setOnClickListener(this);
        this.r.setOnClickListener(this);
        this.S.setOnClickListener(this);
        this.flag = 0;
    }

    public void onClick(View v) {
        if (this.flag != 1) {
            this.flag = 1;
            ((TextView) findViewById(R.id.textView3)).setText("");
            TextView tv = (TextView) findViewById(R.id.textView);
            this.m = 0;
            this.n = new Random().nextInt(3);
            ((TextView) findViewById(R.id.textView2)).setText(new String[]{"CPU: Paper", "CPU: Rock", "CPU: Scissors"}[this.n]);
            if (v == this.P) {
                tv.setText("YOU: Paper");
                this.m = 0;
            }
            if (v == this.r) {
                tv.setText("YOU: Rock");
                this.m = 1;
            }
            if (v == this.S) {
                tv.setText("YOU: Scissors");
                this.m = 2;
            }
            this.handler.postDelayed(this.showMessageTask, 1000);
        }
    }
}
