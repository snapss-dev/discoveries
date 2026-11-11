\\ A072633: a(n) = smallest m with 1^n + 2^n + ... + m^n >= (m+1)^n.
\\ Check that the conjectured formula 1 + round(n/log(2)) fails at the 330-digit n below.
\\ R(m) = sum_{k=1..m} (k/(m+1))^n.  The sum is truncated once a term drops below 10^-1400;
\\ terms decrease roughly like 2^-j, so the neglected tail is far below the margins printed.
\\ Run:  gp -q check.gp
default(realprecision, 1500);
n = 825938178725862470668731143853500055770827366427774395569242416121947420931438276432101429051717195553612323601798832846355583992322952343538822134069965039223614070919286865817634667434475142051826747655585028110155598130153493113423366879864589933523243147286414596703368678554144766303539160428257852463856280045877280683594018;
F = 1 + round(n/log(2));
R(m) = { my(M = m + 1, s = 0., t); for(j = 1, 5000, t = exp(n*log(1 - j/M)); s += t; if(t < 1e-1400, break)); s };
d0 = R(F) - 1; d1 = R(F + 1) - 1;
default(realprecision, 12);
print("digits of n: ", #Str(n));
print("R(F)   - 1 = ", d0, "   (negative: m = F is too small)");
print("R(F+1) - 1 = ", d1, "   (positive: hence a(n) = F + 1)");
\\ sanity check: the formula against the definition for n = 0..300
a(n) = { my(m = 1, s = 1); while(s < (m+1)^n, m++; s += m^n); m };
default(realprecision, 38);
print("formula = definition for n = 0..300: ", sum(n = 0, 300, a(n) != 1 + round(n/log(2))) == 0);
quit
