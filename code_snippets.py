# import pyhf
# pyhf.tensorlib.name
# means = [5, 8]
# stds = [1, 0.5]
# values = [4, 9]
# for backend in ["numpy", "tensorflow", "pytorch", "jax"]:
#     pyhf.set_backend(backend)
#     tb = pyhf.tensorlib
#     normals = tb.normal_dist(tb.astensor(means), tb.astensor(stds))
#     normals.log_prob(tb.astensor(values))

import pyhf
model = pyhf.simplemodels.hepdata_like(
    signal_data=[12.0, 11.0], bkg_data=[50.0, 52.0], bkg_uncerts=[3.0, 7.0]
)
observations = [51, 48]
data = observations + model.config.auxdata
parameters = model.config.suggested_init()  # nominal parameters
model.logpdf(parameters, data)

import pyhf
model = pyhf.simplemodels.hepdata_like(
    signal_data=[12.0, 11.0], bkg_data=[50.0, 52.0], bkg_uncerts=[3.0, 7.0]
)
observations = [51, 48]
data = observations + model.config.auxdata
bestfit_pars, twice_nll = pyhf.infer.mle.fit(data, model, return_fitted_val=True)
model.logpdf(bestfit_pars, data)
-2 * model.logpdf(bestfit_pars, data) == twice_nll
