% matlab_checks.m -- third-engine symbolic verification (MATLAB Symbolic Math
% Toolbox, independent of the sympy harnesses) for the T-IT manuscript
% "The Common-Reconstruction Rate--Distortion Function with Noisy Context"
% (tit-cr-context.tex). Checks the load-bearing closed-form algebra of
% Sections IV-V:
%
%   1. lem:gauss, scalar instantiation (proof of Theorem thm:function):
%      det Sigma_{T|S} = tau^2 (1-rho^2)/s,  det M = s(Q1+n),  and the
%      determinant identity det Sigma_e = n * det Sigma_{T|S} / (Q1+n)
%      with Sigma_e = Sigma_T - J M^-1 J' the linear-estimation error
%      covariance of T from (Yhat, S).
%   2. The FOC linearity solution (eq:ab): (a,b) = (1-1/g, mu_c/g) with
%      mu_c = rho(g-1)/k, k = gs-1, satisfies the stationarity system
%      (eq:foc) and the defining relation mu_c = (a rho + b)/s.
%   3. The constraint-to-quadratic reduction identity (numver table row 2):
%      (g-1)(D-h) - Q1 = (g-1) P(g) / (g k), with h, Q0, Q1 evaluated at
%      the FOC coefficients and P the quadratic (eq:Pg).
%   4. The four gradient identities (eq:grad-ids), with mu_c = (a rho + b)/s
%      as a function of (a,b):
%      d/da(Q0-h)=2, d/db(Q0-h)=2 rho,
%      d/da(Q1-h)=2(1-rho mu_c), d/db(Q1-h)=2(rho-mu_c).
%
% Every check prints PASS/FAIL via isAlways(simplify(...) == 0).

fprintf('=== tit-cr-context MATLAB symbolic checks ===\n');

syms a b n rho tau D g real
s = 1 + tau^2;

names = {}; exprs = {};

%% Check 1: lem:gauss scalar instantiation (Sec. IV, proof of thm:function)
SigmaT  = [1 rho; rho 1];
SigmaTS = [rho; 1];
Sigma_TgS = SigmaT - SigmaTS*SigmaTS.'/s;          % conditional covariance
names{end+1} = 'det Sigma_{T|S} = tau^2(1-rho^2)/s';
exprs{end+1} = det(Sigma_TgS) - tau^2*(1-rho^2)/s;

Q0 = a^2 + b^2 + 2*a*b*rho;                        % Var(aY+bV)
Q1 = Q0 - (a*rho + b)^2/s;                         % Var(aY+bV | S)
% Moments of (T, S, Yhat) with Yhat = aY + bV + N', Var N' = n,
% Cov(N',T) = Cov(N',S) = 0 (the Markov moment identity):
J = [a + b*rho, rho; a*rho + b, 1];                % Cov(T,(Yhat,S))
M = [Q0 + n, a*rho + b; a*rho + b, s];             % Cov((Yhat,S))
names{end+1} = 'det M = s(Q1+n)';
exprs{end+1} = det(M) - s*(Q1+n);

Sigma_e = SigmaT - J*(M\J.');                      % error covariance
names{end+1} = 'det Sigma_e = n det Sigma_{T|S}/(Q1+n)';
exprs{end+1} = det(Sigma_e) - n*det(Sigma_TgS)/(Q1+n);

%% Check 2: the FOC linearity solution (eq:foc)-(eq:ab)
k   = g*s - 1;
mu  = rho*(g-1)/k;                                 % eq:mu
a0  = 1 - 1/g;                                     % eq:ab
b0  = mu/g;                                        % eq:ab
names{end+1} = 'FOC eq (a): a + b rho = 1 - (1 - rho mu_c)/g';
exprs{end+1} = (a0 + b0*rho) - (1 - (1 - rho*mu)/g);
names{end+1} = 'FOC eq (b): a rho + b = rho - (rho - mu_c)/g';
exprs{end+1} = (a0*rho + b0) - (rho - (rho - mu)/g);
names{end+1} = 'mu_c consistency: mu_c = (a rho + b)/s';
exprs{end+1} = mu - (a0*rho + b0)/s;

%% Check 3: the constraint-to-quadratic reduction identity
h0  = (1-a0)^2 - 2*(1-a0)*b0*rho + b0^2;           % eq:distortion h(a,b)
Q0f = a0^2 + b0^2 + 2*a0*b0*rho;
Q1f = Q0f - (a0*rho + b0)^2/s;
Pg  = D*s*g^2 - (D + s - rho^2)*g + (1 - rho^2);   % eq:Pg
names{end+1} = '(g-1)(D-h) - Q1 = (g-1)P(g)/(gk)';
exprs{end+1} = (g-1)*(D - h0) - Q1f - (g-1)*Pg/(g*k);

%% Check 4: the four gradient identities (eq:grad-ids)
h    = (1-a)^2 - 2*(1-a)*b*rho + b^2;
mu_c = (a*rho + b)/s;
names{end+1} = 'd/da (Q0 - h) = 2';
exprs{end+1} = diff(Q0 - h, a) - 2;
names{end+1} = 'd/db (Q0 - h) = 2 rho';
exprs{end+1} = diff(Q0 - h, b) - 2*rho;
names{end+1} = 'd/da (Q1 - h) = 2(1 - rho mu_c)';
exprs{end+1} = diff(Q1 - h, a) - 2*(1 - rho*mu_c);
names{end+1} = 'd/db (Q1 - h) = 2(rho - mu_c)';
exprs{end+1} = diff(Q1 - h, b) - 2*(rho - mu_c);

%% Run all checks
npass = 0; nfail = 0;
for i = 1:numel(names)
    ok = isAlways(simplify(exprs{i}) == 0);
    if ok
        fprintf('PASS  %s\n', names{i}); npass = npass + 1;
    else
        fprintf('FAIL  %s\n', names{i}); nfail = nfail + 1;
    end
end

%% Summary
fprintf('=== %d PASS, %d FAIL ===\n', npass, nfail);
if nfail == 0
    fprintf('ALL CHECKS PASS\n');
else
    error('SOME CHECKS FAILED');
end

% ---------------------------------------------------------------------------
% RUN RECORD (Atlas workstation, 2026-08-26)
% MATLAB R2026a Update 3 + Symbolic Math Toolbox, headless
% `matlab -batch "run('/tmp/matlab_checks.m')"` on Atlas
% (HP Z840, Ubuntu; the manuscript's Lean/Mathlib build host).
% Verbatim output:
%
%   === tit-cr-context MATLAB symbolic checks ===
%   PASS  det Sigma_{T|S} = tau^2(1-rho^2)/s
%   PASS  det M = s(Q1+n)
%   PASS  det Sigma_e = n det Sigma_{T|S}/(Q1+n)
%   PASS  FOC eq (a): a + b rho = 1 - (1 - rho mu_c)/g
%   PASS  FOC eq (b): a rho + b = rho - (rho - mu_c)/g
%   PASS  mu_c consistency: mu_c = (a rho + b)/s
%   PASS  (g-1)(D-h) - Q1 = (g-1)P(g)/(gk)
%   PASS  d/da (Q0 - h) = 2
%   PASS  d/db (Q0 - h) = 2 rho
%   PASS  d/da (Q1 - h) = 2(1 - rho mu_c)
%   PASS  d/db (Q1 - h) = 2(rho - mu_c)
%   === 11 PASS, 0 FAIL ===
%   ALL CHECKS PASS
% ---------------------------------------------------------------------------
