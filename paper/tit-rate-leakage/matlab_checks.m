% matlab_checks.m -- MATLAB Symbolic Math Toolbox cross-checks for tit-rate-leakage.tex (2026-10-02).
% Covers the closed-form and scalar algebra of the paper. The matrix-analytic theorems (tilted water-filling,
% convexity, rank bound, convergence of the iteration) are verified by proof and by the Python scripts.
% Run:  matlab -batch "run('matlab_checks.m')"
pass = 0; fail = 0;

syms Delta u v rho alpha mu positive
syms th pii xi positive
syms x mu1 a positive

% C1 (Thm scalarpath) at a root rho(1-Delta v) = (1-alpha)(1-Delta u):  (1-Delta v)/(1-Delta u) = (1-alpha)/rho
rootrel = (1 - Delta*v) == (1 - alpha)*(1 - Delta*u)/rho;
L_expr = (1 - Delta*v)/(1 - Delta*u);
ok = isAlways(subs(L_expr, v, solve(rootrel, v)) == (1 - alpha)/rho);
[pass, fail] = report('C1 scalarpath: at a root, (1-Delta v)/(1-Delta u) = (1-alpha)/rho', ok, pass, fail);

% C2 (Thm scalarpath, alpha = 0) with rho = mu/(Delta+mu): rho(1-Delta v)-(1-Delta u) = Delta(Delta u + mu(u-v) - 1)/(Delta+mu)
lhs = (mu/(Delta + mu))*(1 - Delta*v) - (1 - Delta*u);
rhs = Delta*(Delta*u + mu*(u - v) - 1)/(Delta + mu);
ok = isAlways(simplify(lhs - rhs) == 0);
[pass, fail] = report('C2 scalarpath alpha=0: root equation equals Delta u + mu(u-v) = 1 (secular form)', ok, pass, fail);

% C3 pencil relation: 1-Delta u = mu(u-v) and 1-Delta v = (mu+Delta)(u-v) give rho = (1-Delta u)/(1-Delta v) = mu/(Delta+mu)
syms w positive   % w = u - v
ok = isAlways(simplify((mu*w)/((mu + Delta)*w) - mu/(Delta + mu)) == 0);
[pass, fail] = report('C3 rho = mu_max/(Delta+mu_max) from the two pencil identities', ok, pass, fail);

% C4 (Thm lowdist / Thm commuting) quadratic th*pii*xi^2 + (th - alpha*pii)*xi - 1 = 0  <=>  alpha + (1-alpha)/(1+pii*xi) = th*xi
quad = th*pii*xi^2 + (th - alpha*pii)*xi - 1;
stat = (alpha + (1 - alpha)/(1 + pii*xi) - th*xi)*(1 + pii*xi);
ok = isAlways(simplify(stat + quad) == 0);
[pass, fail] = report('C4 lowdist/commuting: quadratic is the stationarity condition times (1+pi xi)', ok, pass, fail);

% C5 product of the roots of the quadratic is -1/(th*pii) < 0: exactly one positive root
c = coeffs(quad, xi, 'All');   % [th*pii, th-alpha*pii, -1]
ok = isAlways(c(3)/c(1) == -1/(th*pii));
[pass, fail] = report('C5 lowdist: product of roots -1/(theta pi) < 0, so a unique positive root', ok, pass, fail);

% C6 (Prop fixedread) (1+Delta/mub)/(1+Delta/mu1) = 1 + Delta x/((mu1-x)(mu1+Delta)) with x = mu1 - mub
mub = mu1 - x;
ok = isAlways(simplify((1 + Delta/mub)/(1 + Delta/mu1) - (1 + Delta*x/((mu1 - x)*(mu1 + Delta)))) == 0);
[pass, fail] = report('C6 fixedread: exact ratio identity', ok, pass, fail);

% C7 x/(mu1-x) is increasing on [0, mu1): derivative mu1/(mu1-x)^2 > 0
ok = isAlways(simplify(diff(x/(mu1 - x), x) - mu1/(mu1 - x)^2) == 0);
[pass, fail] = report('C7 fixedread: d/dx [x/(mu1-x)] = mu1/(mu1-x)^2 > 0', ok, pass, fail);

% C8 (Cor scalar vs secular equation, p = 2) Sigma = [1 r; r 1], q = e1, K = (Sigma^-1 + J)^-1, J = diag(0, 1/t2).
% With mu = Delta/(g-1) and Delta = 1-D, q'S(Delta S + mu K)^-1 S q - 1 vanishes exactly when P(g) does.
syms r t2 D g real
S = [1 r; r 1]; J = [0 0; 0 1/t2]; K = inv(inv(S) + J); q = [1; 0];
Dl = 1 - D; muv = Dl/(g - 1);
sec = simplify(q.'*S*inv(Dl*S + muv*K)*S*q - 1);
s = 1 + t2; P = D*s*g^2 - (D + s - r^2)*g + (1 - r^2);
[nsec, dsec] = numden(sec);
ratio = simplify(nsec/P);
ok = ~has(ratio, g) && ~isAlways(ratio == 0);   % numerator is P(g) times a factor free of g
fprintf('     secular numerator / P(g) = %s\n', char(ratio));
[pass, fail] = report('C8 p=2: secular equation numerator is P(g) times a g-free factor', ok, pass, fail);

% C9 (paragraph after Thm tilted) Woodbury: H'(H X H' + SU)^-1 H = X^-1 (X - Xe) X^-1, Xe = (X^-1 + H' SU^-1 H)^-1
syms x11 x12 x22 h1 h2 su real
X = [x11 x12; x12 x22]; H = [h1 h2];
Xe = inv(inv(X) + H.'*(1/su)*H);
lhsW = H.'*inv(H*X*H.' + su)*H; rhsW = inv(X)*(X - Xe)*inv(X);
ok = all(all(isAlways(simplify(lhsW - rhsW) == 0)));
[pass, fail] = report('C9 tilt: Woodbury identity for a rank-one holder, 2x2 X (symbolic)', ok, pass, fail);

% C10 (Prop mm) majorizer: ln(h x + s) <= ln(h x0 + s) + h (x - x0)/(h x0 + s) (tangent of a concave function), h, s > 0
syms hh ss x0 positive
gap = log(hh*x0 + ss) + hh*(x - x0)/(hh*x0 + ss) - log(hh*x + ss);
d2 = simplify(diff(log(hh*x + ss), x, 2));
ok = isAlways(d2 < 0) && isAlways(subs(gap, x, x0) == 0) && isAlways(simplify(subs(diff(gap, x), x, x0)) == 0);
[pass, fail] = report('C10 mm: log(hx+s) is concave and its tangent at x0 touches with matching slope', ok, pass, fail);

% C11 (Thm scalarpath / Thm onedim) rate at the active noise level: sigma^2 = (1-Delta u)/Delta gives
% 1/2 log(1 + u/sigma^2) = -1/2 log(1 - Delta u)
sig2 = (1 - Delta*u)/Delta;
ok = isAlways(simplify((1 + u/sig2) - 1/(1 - Delta*u)) == 0);
[pass, fail] = report('C11 scalarpath: 1 + u/sigma^2 = 1/(1 - Delta u) at the active noise level', ok, pass, fail);

fprintf('TOTAL: %d passed, %d failed\n', pass, fail);

function [pass, fail] = report(name, ok, pass, fail)
    if ok, fprintf('PASS %s\n', name); pass = pass + 1; else, fprintf('FAIL %s\n', name); fail = fail + 1; end
end
