default(realprecision,220);
print("A175639 ", prodeulerrat(1-3/p^3+2/p^4+1/p^5-1/p^6));
print("A078076 ", contfrac(prodeulerrat(1 - 1/(p^2-2)),,110));
print("A078077 ", contfrac(prodeulerrat(1 + 1/(p^2+p-1)),,110));
print("A078086 ", contfrac(prodeulerrat(1 - 1/(p^2*(p^2-1))),,110));
print("A078088 ", contfrac((5 * Pi^2 / 48) * prodeulerrat(1 - (p+2)/p^3, 1, 3),,110));
