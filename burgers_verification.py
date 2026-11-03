
"""
Rigorous solution + verification of the viscous Burgers equation
    u_t + u u_x = nu u_xx,  x in [0, 2*pi) periodic,  u(x,0) = sin(x).

Exact closed form via the Cole-Hopf transform, verified independently:
  (1) symbolic check of the transform identity (sympy)
  (2) independent spectral time-stepper vs the closed form
  (3) invariants (mass, energy balance), limiting cases, small-nu shock
"""
import numpy as np
from scipy.special import ive

nu = 0.1
T = 2.0

# ==================================================================
# PART 1: Cole-Hopf identity, checked symbolically
# ==================================================================
print("=" * 72)
print("PART 1: symbolic check of the Cole-Hopf identity")
print("=" * 72)
try:
    import sympy as sp
    xs, ts, nus = sp.symbols('x t nu', positive=True)
    th = sp.Function('theta')(xs, ts)
    u = -2 * nus * sp.diff(th, xs) / th
    resid = sp.diff(u, ts) + u * sp.diff(u, xs) - nus * sp.diff(u, xs, 2)
    target = -2 * nus * sp.diff(sp.diff(th, ts) - nus * sp.diff(th, xs, 2), xs) / th
    delta = sp.simplify(resid - target)
    ok = sp.simplify(delta) == 0
    print("identity  u_t + u u_x - nu u_xx = -2 nu d_x[(theta_t - nu theta_xx)/theta]:",
          "CONFIRMED (sympy)" if ok else f"FAILED, delta = {delta}")

    # concrete: theta = 2 + e^{-nu t} cos x is a positive heat solution;
    # the induced u must solve Burgers exactly.
    thc = 2 + sp.exp(-nus * ts) * sp.cos(xs)
    uc = -2 * nus * sp.diff(thc, xs) / thc
    rc = sp.simplify(sp.diff(uc, ts) + uc * sp.diff(uc, xs) - nus * sp.diff(uc, xs, 2))
    print("concrete positive heat solution -> Burgers residual:", rc)
except ImportError:
    print("sympy not installed - skipping symbolic check")

# ==================================================================
# PART 2: exact series solution, u0 = sin(x)
#   theta(x,0) = exp((cos x - 1)/(2 nu))
#   e^{beta cos x} = sum_{n in Z} I_n(beta) e^{i n x},  beta = 1/(2 nu)
#   theta(x,t)  propto  I_0(beta) + 2 sum_{n>=1} I_n(beta) e^{-nu n^2 t} cos(n x)
#   u = -2 nu theta_x / theta
# ==================================================================
print()
print("=" * 72)
print("PART 2: exact series solution")
print("=" * 72)


def u_exact(x, t, nu, N=150):
    beta = 1.0 / (2.0 * nu)
    n = np.arange(0, N + 1)
    In = ive(n, beta)                    # scaled: I_n(beta) e^{-beta}
    dec = np.exp(-nu * (n ** 2) * t)
    x = np.atleast_1d(np.asarray(x, float))
    th = In[0] + 2.0 * np.sum((In * dec) * np.cos(np.outer(x, n)), axis=1)
    thx = -2.0 * np.sum((n * In * dec) * np.sin(np.outer(x, n)), axis=1)
    return -2.0 * nu * thx / th


xg = np.linspace(0.0, 2.0 * np.pi, 4096, endpoint=False)
err0 = np.max(np.abs(u_exact(xg, 0.0, nu) - np.sin(xg)))
print(f"t=0 consistency:  max |u_exact - sin(x)| = {err0:.2e}   (expect ~1e-12)")
for tt in [0.5, 1.0, 2.0, 5.0]:
    print(f"  t={tt:4.1f}:  max|u| = {np.max(np.abs(u_exact(xg, tt, nu))):.6f}")
print("  (max|u| decaying -> diffusion wins on the periodic domain, as it must)")

# ==================================================================
# PART 3: independent numerical solve (Fourier pseudospectral,
# per-step integrating factor, RK4, 2/3 dealiasing)
# ==================================================================
print()
print("=" * 72)
print("PART 3: independent spectral solver vs closed form, nu = 0.1")
print("=" * 72)


def solve_burgers_spectral(nu, t_end, N=1024, dt=1e-3):
    x = 2.0 * np.pi * np.arange(N) / N
    k = np.fft.fftfreq(N) * N
    deal = np.abs(k) <= N // 3
    k2 = k * k

    def rhs(v, tau):
        # v(tau) = e^{nu k^2 tau} uhat(t0+tau);  u = ifft(v e^{-nu k^2 tau})
        uu = np.fft.ifft(v * np.exp(-nu * k2 * tau)).real
        nl = -0.5j * k * np.fft.fft(uu * uu)
        nl[~deal] = 0.0
        return np.exp(nu * k2 * tau) * nl

    uhat = np.fft.fft(np.sin(x))
    uhat[~deal] = 0.0
    for _ in range(int(round(t_end / dt))):
        v = uhat
        k1 = rhs(v, 0.0)
        k2_ = rhs(v + 0.5 * dt * k1, 0.5 * dt)
        k3 = rhs(v + 0.5 * dt * k2_, 0.5 * dt)
        k4 = rhs(v + dt * k3, dt)
        v_end = v + dt * (k1 + 2 * k2_ + 2 * k3 + k4) / 6.0
        uhat = v_end * np.exp(-nu * k2 * dt)
    return x, np.fft.ifft(uhat).real


for tt in [0.5, 1.0, 2.0]:
    xn, un = solve_burgers_spectral(nu, tt, dt=1e-3)
    ue = u_exact(xn, tt, nu)
    print(f"t={tt:4.1f}:  max |u_numerical - u_exact| = {np.max(np.abs(un - ue)):.3e}")

# convergence order check
xn, un1 = solve_burgers_spectral(nu, 1.0, dt=1e-3)
xn, un2 = solve_burgers_spectral(nu, 1.0, dt=2.5e-4)
ue = u_exact(xn, 1.0, nu)
e1, e2 = np.max(np.abs(un1 - ue)), np.max(np.abs(un2 - ue))
print(f"RK4 order check: err(dt=1e-3)={e1:.3e}, err(dt=2.5e-4)={e2:.3e}, "
      f"ratio={e1 / max(e2, 1e-300):.1f}  (4th order -> ~256)")

# mass conservation on the numerical solution
print(f"mass:  max |mean(u)(t=2) - mean(u)(t=0)| = {abs(np.mean(un1) - 0.0):.2e}")

# ==================================================================
# PART 4: energy balance  dE/dt = -nu * int u_x^2 dx
# ==================================================================
print()
print("=" * 72)
print("PART 4: energy balance check on the exact solution")
print("=" * 72)
ts = np.linspace(0.0, 2.0, 401)


def energy(u):
    return 0.5 * (2.0 * np.pi) * np.mean(u ** 2)


def int_ux2(t):
    u = u_exact(xg, t, nu)
    uh = np.fft.fft(u)
    k = np.fft.fftfreq(len(xg)) * len(xg)
    ux = np.fft.ifft(1j * k * uh).real
    return (2.0 * np.pi) * np.mean(ux ** 2)


E = np.array([energy(u_exact(xg, t, nu)) for t in ts])
diss = np.array([int_ux2(t) for t in ts])
lhs = E[-1] - E[0]
rhs = -nu * np.trapezoid(diss, ts)
print(f"E(2) - E(0)              = {lhs:.10f}")
print(f"-nu * int_0^2 int u_x^2  = {rhs:.10f}")
print(f"relative mismatch         = {abs(lhs - rhs) / abs(lhs):.2e}")
print(f"E(t) monotone decreasing: {bool(np.all(np.diff(E) < 0))}")

# ==================================================================
# PART 5: small viscosity -> inviscid shock formation
# ==================================================================
print()
print("=" * 72)
print("PART 5: nu = 0.01 - gradient catastrophe capped by viscosity")
print("=" * 72)
nu2 = 0.01
print("inviscid prediction (u0 = sin x): breaking time t* = 1 at x = pi;")
print("u_x at the shock origin = -1/(1-t)  ->  -10 at t=0.9, -100 at t=0.99")
print()
print(f"{'t':>6} {'max|u_x| (viscous, nu=0.01)':>28} {'inviscid -1/(1-t)':>22}")
for tt in [0.5, 0.9, 0.99, 1.0, 1.05, 1.2, 2.0]:
    u = u_exact(xg, tt, nu2)
    uh = np.fft.fft(u)
    k = np.fft.fftfreq(len(xg)) * len(xg)
    ux = np.fft.ifft(1j * k * uh).real
    inv = -1.0 / (1.0 - tt) if tt < 1.0 else float("-inf")
    inv_s = f"{inv:.1f}" if np.isfinite(inv) else "-inf (blow-up)"
    print(f"{tt:6.2f} {np.max(np.abs(ux)):28.2f} {inv_s:>22}")

u = u_exact(xg, 1.2, nu2)
uh = np.fft.fft(u)
k = np.fft.fftfreq(len(xg)) * len(xg)
ux = np.fft.ifft(1j * k * uh).real
i_front = np.argmax(np.abs(ux))
print(f"\nt=1.2, nu=0.01: front at x = {xg[i_front]:.4f}  (predicted pi = 3.1416)")
print(f"  min u_x = {ux.min():.2f};  Taylor steady-shock estimate -du^2/(8 nu) = "
      f"{-4.0 / (8 * nu2):.1f}")
half = np.max(np.abs(ux)) / 2
mask = np.abs(ux) > half
width = xg[mask][-1] - xg[mask][0]
print(f"  measured front width ~ {width:.3f};  Taylor estimate 4 nu / du = {4 * nu2 / 2.0:.3f}")
print(f"  antisymmetry u(2pi-x) = -u(x):  max deviation = "
      f"{np.max(np.abs(u + u[::-1])):.2e}  (=> Rankine-Hugoniot shock speed = 0)")
