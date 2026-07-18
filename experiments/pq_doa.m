% Mature Phased Array DOA on each covariance from PolarQuant DOA Gate-B
% (experiments/polarquant_doa_gateb.py). The 8 cm DICIT ULA at exactly lambda/2 (2144 Hz)
% makes espritdoa / rootmusicdoa (which assume a half-wavelength ULA) exact. Runs on Atlas.
d = load('/tmp/pq_covs.mat');
R = d.R;                       % K x M x M complex
nsig = double(d.nsig);
K = size(R, 1);
esprit = nan(K, 1);
rootmusic = nan(K, 1);
for k = 1:K
    Rk = squeeze(R(k, :, :));
    Rk = (Rk + Rk') / 2;       % hermitianize
    try, a = espritdoa(Rk, nsig);    esprit(k)    = a(1); catch, end
    try, b = rootmusicdoa(Rk, nsig); rootmusic(k) = b(1); catch, end
end
save('/tmp/pq_doas.mat', 'esprit', 'rootmusic');
fprintf('pq_doa: estimated %d covariances\n', K);
