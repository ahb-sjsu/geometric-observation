% GO-P-2026-031 independent-estimator reference — MATLAB Phased Array root-MUSIC.
% Consumer C = root-MUSIC (continuous/off-grid, multi-snapshot SUBSPACE method) — nothing like
% the numpy beamformer-ML in doa_gateb.py. Same corrected read operator ghat = P_a^perp a'(th0),
% same matched-bits three-arm shaping in the R^{2M} embedding, same HELD-OUT params
% (M=16, theta0=-7 deg, kappa=4). If root-MUSIC ALSO shows angle MSE invariant<recon<anti with
% reconstruction minimized by recon, the flip is estimator-agnostic. The REC_* columns must match
% doa_gateb.py's (reconstruction energy is a property of the arms, not the estimator).
% Run on Atlas via the atlas skill: run_matlab.py experiments/doa_gateb_rootmusic.m
rng(7);
M = 16; dsp = 0.5; pos = (0:M-1)*dsp; th0 = -7;    % deg, ULA half-wavelength (HELD-OUT)
kappa = 4; T = 32; nTrials = 500; noise = 0.01;
a  = steervec(pos, th0);
h  = 1e-4;
da = (steervec(pos, th0+h) - steervec(pos, th0-h)) / (2*h);
Pperp_da = da - a*((a'*da)/(a'*a));
ghat = Pperp_da / norm(Pperp_da);
c2r = @(z)[real(z); imag(z)];
r2c = @(v)v(1:M) + 1i*v(M+1:end);
w = c2r(ghat); w = w/norm(w);
R0 = randn(2*M); R0(:,1) = w; [Q,~] = qr(R0); Q(:,1) = w;
dP = 2*M-1;
s0sqs = logspace(-1,-4,6);
modes = {'invariant','recon','anti'};
try, rootmusicdoa(a*a' + eye(M), 1); catch e, error(['rootmusicdoa unavailable: ' e.message]); end

MSE = zeros(6,3); REC = zeros(6,3);
for ie = 1:6
  s0sq = s0sqs(ie);
  for im = 1:3
    switch modes{im}
      case 'invariant', eR = s0sq/kappa;   eP = s0sq*kappa^( 1/dP);
      case 'recon',     eR = s0sq;         eP = s0sq;
      case 'anti',      eR = s0sq*kappa;   eP = s0sq*kappa^(-1/dP);
    end
    sd = sqrt([eR; eP*ones(dP,1)]);
    es = 0; rc = 0;
    for tr = 1:nTrials
      s = (randn(1,T)+1i*randn(1,T))/sqrt(2);
      X = a*s + noise*(randn(M,T)+1i*randn(M,T))/sqrt(2);
      D = zeros(M,T);
      for t = 1:T, D(:,t) = r2c(Q*(sd.*randn(2*M,1))); end
      Xh = X + D;
      doa = rootmusicdoa((Xh*Xh')/T, 1);
      es = es + (doa(1)-th0)^2;
      rc = rc + mean(sum(abs(D).^2,1));
    end
    MSE(ie,im) = es/nTrials; REC(ie,im) = rc/nTrials;
  end
end
fprintf('GO-P-2026-031 rootMUSIC ref | M=%d th0=%d kappa=%g T=%d (HELD-OUT)\n', M, th0, kappa, T);
fprintf('%4s | %10s %10s %10s | %8s %8s %8s\n','rate','MSE_inv','MSE_rec','MSE_anti','REC_inv','REC_rec','REC_anti');
flip = 0;
for ie = 1:6
  ok = (MSE(ie,1)<=MSE(ie,2)) && (MSE(ie,2)<=MSE(ie,3)) && (REC(ie,2)<=REC(ie,1)) && (REC(ie,2)<=REC(ie,3));
  flip = flip + ok;
  fprintf('%4d | %10.3e %10.3e %10.3e | %8.3f %8.3f %8.3f  %s\n', ie, ...
    MSE(ie,1),MSE(ie,2),MSE(ie,3), REC(ie,1),REC(ie,2),REC(ie,3), repmat('<',1,ok));
end
fprintf('FLIP (angle MSE inv<=rec<=anti AND recon-optimal is recon): %d/6 rate points\n', flip);
