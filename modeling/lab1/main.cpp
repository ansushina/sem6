#include <iostream>
#include <math.h>
#include <vector>
#include <algorithm>

using namespace std;

double F( double x, double u) {
    return x*x + u*u;
}

double pikar1(double x) {
    return pow(x, 3)/3.0;
}

double pikar2(double x) {
    return pow(x, 3) / 3.0 * (1 + pow(x, 4) / 21.0);
}

double pikar3(double x) {
    return pow(x, 3) / 3.0 * (1.0 +
                            1.0/21.0 * pow(x, 4) +
                            2.0/693.0 * pow(x, 8) +
                            1.0/19845.0 * pow(x, 12));
}

double pikar4(double x) {
    return (pow(x,3)/3.0 + pow(x,7)/63.0 + pow(x,11)/2079.0*2.0 +
            pow(x,15)/218295.0*13 + pow(x,19)/441.0/84645.0*82.0 +
            pow(x,23)/68607.0/152145.0*662.0 + pow(x,27)/pow(3,11)/18865.0*4.0+
            pow(x,31)/194481.0/564975.0);
}

vector<double> yavnii(vector<double> &x, double step) {
    vector<double> y;
    y.resize(x.size());
    y[0] = 0;
    for (int i = 1; i < x.size(); i++) {
        y[i] = y[i-1] + step * F(x[i-1], y[i-1]);
    }
    return y;
}

vector<double> neyavnii(vector<double> &x, double step) {
    vector<double> y;
    y.resize(x.size());
    y[0] = 0;
    for (int i = 1; i < x.size(); i++) {
        y[i] = 1.0/2.0/step - sqrt(1.0/4.0/step/step - y[i-1]/step - x[i]*x[i]);
    }
    return y;
}

int main()
{
    setbuf(stdout, NULL);
    //cout << "Hello World!" << endl;
    double xfrom, xto, step;
    cout << "Input:\nx from ";
    cin >> xfrom;
    cout << "x to   ";
    cin >> xto;
    cout << "step   ";
    cin >> step;

    vector<double> x;
    for (double i = xfrom; i <= xto; i = i + step){
        x.push_back(i);
    }

    vector<double> p1, p2, p3, p4, neya, ya;

    for (int i = 0; i < x.size(); i++) {
        p1.push_back(pikar1(x[i]));
        p2.push_back(pikar2(x[i]));
        p3.push_back(pikar3(x[i]));
        p4.push_back(pikar4(x[i]));
    }

    ya = yavnii(x, step);
    neya = neyavnii(x, step);

    printf("|%8s|%15s|%15s|%15s|%15s|%15s|%15s|\n", "n", "yavnii", "neyavnii", "pikar1", "pikar2", "pikar3", "pikar4");

    for (int i = 0; i < x.size(); i++) {
        printf("|%8f|%15f|%15f|%15f|%15f|%15f|%15f|\n", x[i], ya[i], neya[i], p1[i], p2[i], p3[i], p4[i]);
    }

    return 0;
}
