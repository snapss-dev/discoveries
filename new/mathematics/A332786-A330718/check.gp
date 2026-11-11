/* A332786: a(n) = numerator(-1/n + sum_{k=1..n} 2^(k-1)/k).
   A330718: b(n) = numerator(sum_{k=1..n} (2^(k-1)-1)/k).
   For n = p^2 put T = p^2 * (the rational number). T is a p-adic integer, and the p-adic valuation
   of the numerator is v_p(T) - 2 whenever v_p(T) >= 2.
   For A332786:  T  = sum over k not divisible by p of p^2 2^(k-1)/k
                    + sum over j < p of p 2^(pj-1)/j  +  2^(n-1)  -  1.
   For A330718:  T' = T - p^2 H(n-1), that is, 2^(k-1) is replaced by 2^(k-1) - 1 in every term.
   Both are computed modulo p^5 with one plain loop over k = 1..n. */
vT(p) = { my(n = p^2, M = p^5, s = Mod(0, M), h = Mod(0, M), t = Mod(1, M), u);
  for(k = 1, n,
    if(k % p,
      u = Mod(1, M) / k; s += p^2 * t * u; h += p^2 * u,
      if(k < n, u = Mod(1, M) / (k \ p); s += p * t * u; h += p * u, s += t));
    t *= 2);
  s -= 1;
  h = s - h;
  [if(lift(s) == 0, 5, valuation(lift(s), p)), if(lift(h) == 0, 5, valuation(lift(h), p))] };
exa(n) = numerator(-1/n + sum(k = 1, n, 2^(k-1)/k));
exb(n) = numerator(sum(k = 1, n, (2^(k-1)-1)/k));
/* calibration against exact rational arithmetic */
forprime(p = 5, 31, my(v = vT(p)); print("p=", p, "  A332786: v_p(a(p^2)) exact=", valuation(exa(p^2), p), " modular=", v[1] - 2, "   A330718: v_p(b(p^2)) exact=", valuation(exb(p^2), p), " modular=", v[2] - 2));
{ my(p = 16843, v = vT(p)); print("p=16843  A332786: v_p(T)=", v[1], "  v_p(a(p^2))=", v[1] - 2, "   A330718: v_p(T')=", v[2], "  v_p(b(p^2))=", v[2] - 2); }
