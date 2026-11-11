default(parisizemax, 3000000000);
{
  T = 10^(10^8-1);
  forstep(k = 13993958, 13993959, 1,
    v = k^k;
    print(k, "  k^k >= 10^(10^8-1): ", v >= T, "   k^k >= 10^(10^8): ", v >= 10*T);
  );
}
\p 80
print(13993959*log(13993959)/log(10));
print(13993958*log(13993958)/log(10));
quit
