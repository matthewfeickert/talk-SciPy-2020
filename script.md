**NOTE TO CAPTIONER: This is an outline script and not 100% the same as the audio in my
video. If you need an _exact_ script this will not be useful. However, this is probably greater
than 90% similar to the final audio.**

## Intro

Hi! I'm Matthew Feickert and I'm a particle physicist. I'm
postdoctoral research associate at the University of Illinois at Urbana-Chmapaign
where I work on the ATLAS experiment as at the
Institute for Research and Innovation in Software for High Energy Physics

## Slide 2

We're all experimental high energy particle physicists
that work together on an experimental collaboration with 3,000 of our closest
colleagues called ATLAS that's located just outside of beautiful Geneva, Switzerland at
CERN's Large Hadron Collider (the LHC).
Here you can see the obligatory picture of the LHC's huge 27 kilometer circumference
drawn over the Swiss-French countryside with markers indicating where the main experiments
reside along the ring about 100 meters below ground.

Our collaboration is formed around the ATLAS detector (seen here with a TRex for scale),
which you can think of as a cathedral sized digital camera for recording the
events of colliding beams of protons from the LHC at almost the speed of light for us to then
later analyze.

We're smashing protons together at extreme energy densities and looking at the splattered
remains in our detector because we want to
understand the fundamental forces of the Universe (like electromagnetism and
the strong and weak nuclear forces) and their interactions with the most elementary
particles of Matter.
With a long history of success we've been able to distill down what we know about
the Universe so far (so that with a bit of manipulation) you can fit it in one equation
on the side of a coffee cup
but we know that's not the full picture.

We're still trying to understand some of the physics we do know about, like the Higgs boson we found in 2012,
as well as see
if we can find evidence for new physics like Dark Matter.

## Slide 3

So we're trying to ask the Universe pretty fundamental questions about what it is,
but the Universe isn't interested in answering them too easily.
We have to run our colliders for years at a time, producing millions of collisions per second,
to try to collect as much high quality data as possible
on the rare events that can give us a glimpse as to the missing parts of our picture.

## Slide 4

When we do analyze all that data, we're looking to extract as much information as possible out of it.
We're using it search for new physics, like when we discovered a new particle that was consistent
with the theoretical predictions of the Higgs boson in 2012,
but we're also using it to make precision measurements of the physics we do know about to better understand
its properties, so that when we don't find evidence of new physics in our searches we can still
provide the best limit constraints on different possible theories.

All of this requires building statistical models and then fitting those models to the data to perform statistical inference.
However, the model complexity for some of the analyses can be huge
resulting in the time to perform these fits being many hours.
This is obviously a problem, ad we want to try to empower analysts (ourselves) with fast fits and expressive models so that we
can decrease the time to inference and insight.

## Slide 5

We turn now HistFactory --- one of the most extensively used statistical models
in all of high energy physics.
This flexible probability density function template was first developed in the field as part of the efforts in the
search for the Higgs boson.
Since the discovery of the Higgs, it has gone on to be used
ubiquitously in both measurements of known physics processed (physics described by the Standard Model)
as well as searches for new physics (which we refer to as BSM --- beyond the Standard Model)

## Slide 6

When we break down what the HistFactory template is though, we see it has a simple form.
Though here we do need to introduce some terminology: the terms "channel" and "sample"

- Here a "channel" just means a "particular selection criteria for the analysis".
If you'll allow me to simplify to avoid giving an aside lightening talk on the Standard Model,
this might mean requiring seeing two particles of one type and a third of another in the detector
and that their combined energy lies within a specific range.
In the plot below we see that _each bin_ is a different analysis region
("a different channel").
Here there is just 1 bin in each channel, but that's just this particular example.
There are analyses in which channels contain many bins.

- Following that, a "sample" corresponds to a particular physics process that
could result in producing particles that would get selected for a particular "channel".
So each of these colored histograms in the histogram stacks in each bin corresponds to a different "sample".
As you can see, some "samples" (physics processes) show up in different channels.

Okay, given this aside, we can backtrack to see the HistFactory template is just
comprised of a main part (in blue) which is the product of Poisson distributions across all bins in all channels,
where the event rate parameter of the Poisson is determined from a nominal event rate that is
affected by different multiplicative and additive modifiers in each sample.
The reason for using Poissons is that we're doing counting experiments for subatomic processes
that are inherently random.

The second part (in red) is comprised of constraint p.d.f.s that allow for different auxiliary measurements
to constrain the overall model and encode different systematic uncertainties from the
physics theory and the detector responses.
So in this example plot, the samples could share a systematic uncertainty in the normalization, in addition to other modifiers.

## Slide 7

This gives us a mathematical grammar to setup a simultaneous fit for multiple channels ("regions") each
with multiple bins and multiple samples ("processes") that are all coupled to a set of constraints.
But the important part is that this is just mathematics!
No software specification is defined anywhere, but until very recently in 2018 the only implementation that
existed of HistFactory was in the monolithic C++ library (called ROOT)
that has been the computational backbone of experimental high energy physics for almost 25 years.
The change was the creation of `pyhf` --- the first pure Python implementation of HistFactory,
which as you can see just a pip install away on PyPI and openly developed on GitHub.

## Slide 8

Okay, now that we've hopefully motivated the existence of pyhf and the HistFactory formalism
let's dive into the pyhf API a bit.
The basic object that is at the heart of everything is, unsurprisingly, the model.
However, what we're interested in doing with the model is going to be maximum likelihood fits
so we'll be dealing a lot with the logpdf as we want to get the log likelihood of the model parameters
conditioned on the observed data.

In this minimal simple example using two bins in a single channel we see that we
can create a simplistic model quickly and then with the data from our experimental observations
and the model auxiliary constraints we can get the log likelihood of the default
initialization parameters of the model.

## Slide 9

If we look at how this model is _actually_ being represented internally though, we
see that it is a directed computational graph that shows the full formalism of HistFactory.
Each node of the graph represents a vectorized n-dimensional array (or as we'll call it "tensor") operation.

You can see from the colored nodes that the data and the model parameters enter at different points,
and are additionally largely factor out into subgraphs.
These parameter and data graphs combine at the bottom of the graph to be used in the computation
of the log likelihood.

## Slide 10

Okay, we can now turn our attention to the core task of performing maximum likelihood fits
with `pyhf`.
Here, we want to minimize the objective function which is twice the negative log likelihood,
as minimizing the _negative_ log likelihood is the same as maximizing the likelihood.

We can see that the `pyhf` API for this is pretty transparent, and looking at
the same minimal example as before, we see that performing the maximum likelihood fit
with our optional `return_fitted_val` key-word-argument returns the maximum likelihood estimate of
the model parameters as well as minus two log likelihood at these best fit parameters.

Here you can see that we explicitly to a demonstration check of that that in the last steps.

## Slide 11

We're now going to use our tools to get at what we really care about:
performing a profile likelihood fit for our parameter of interest $\mu$.
Here we "profile" out the nuisance parameters, $theta$, by expressing the nuisance parameters as functions of the parameter of interest.

From a physics standpoint, the parameter of interest is typically the normalization
factor on the count of the new physics process we're searching for.
Since the new physics is what we're searching for, we call it "the signal", and the Standard Model physics "the background",
we would call this parameter of interest "the signal strength."

Okay, anyway, so what we want to do for this profile likelihood fit is on the
top line perform a constrained best fit for a given signal strength value, $\mu$,
that we're testing to get the the best fit nuisance
parameters given this test value mu, and then compare that to the unconstrained
best fit (on the bottom) where all the model parameters are free parameters in the fit.
So we're doing a hypothesis test for the production rate of our new physics!

We can then take this result as a test statistic and calculate a modified $p$-value
that we call the CL_s using either results from asymptotic distributions or generating
pseudo-experiments.
This is all to ask "given our model and the data, did we discover new physics?"
And we want to do all of this as fast as possible!

That's a lot, but `pyhf` provides a hypothesis test API.

Continuing our example, we see that performing the hypothesis test for a signal strength
consistent with theory, 1, and our return_expected_set key-word-argument we get back
both the observed modified-p-values as well as a band of variations from the expected
result if there was no new physics. This is exactly what we need.

## Slide 12 [START HERE]

As the serialization of the likelihood had previously been in a domain specific binary format
that provided some difficulties for analysis reinterpretation, we gave a lot of thought to how `pyhf` should
do things.
This resulted in the decision to create a JSON schema that would allow for a declarative
specification of the HistFactory model.

On the right we see a short working example of the JSON spec for a single chnnel, two bin counting experiment with a systematic uncertainty (ignoring of course
the highlighted comments which I put in by hand that are obviously invalid JSON).
Given our coverage of the formalism, we see that we have a list of channels, which
have lists of samples, with associated lists of rate factors and systematic uncertainties,
as well as the observed data, our declared parameter of interest, and the schema version.
All of HistFactory is represented here, so we have a declarative full serialization of the likelihood!

JSON provides us many advantages. It is both human and machine readable, making
it mentally much easier to deal with.
Additionally, JSON is an industry standard and will be with us till the heat death
of the Universe, so we have long long term support baked in.
In the same vein, it is parsable in pretty much every language, so if alternative
implementations exist our models can be easily ported.
Finally, given the large cost of running the LHC and building experimental detectors the size of buildings
we want to try and reuse analyses as much as possible in the future.
JSON is plain text and so versionable, easily preserved, and highly
compressible, making it a great choice.

## Slide 13

Another great thing about using JSON is that we then also get JSON Patch, which
allows us to easily mutate our models!

If we take the example JSON spec we just looked at and use the `pyhf` command line API
to perform a CLs computation we get an observed value given the background and signal models
considered (we could call this "signal model A").
If we want to now test some new physics model ("signal model B") that would have different
contributions then we can use JSON patch to "patch" in this new signal on the fly
and recompute our result.

So we see that the observed modified p-value (the CLs) that we get for this new patched-in signal
model is different from the original signal model result.

## Slide 14

In a typical physics analysis we additionally want to evaluate signal hypotheses
for a range of possible particle masses, which results in hundreds of points in
our parameter space to evaluate.

The choice of JSON allows for us to further simplify things by breaking out the
background only model JSON into one file and then creating a "patch set" file that
contains all of the signal model JSON Patches inside of it.

These two JSON files along with the pyhf schema fully preserve the analysis likelihood,
making it reusable by theorists and experimentalists alike.
These full likelihoods can then be publicly published to HEPData --- a repository for
data associated with particle physics results --- which will mint a DOI for these data products as well!

When validating that the results obtained with pyhf were consistent with results
from the C++ library, we saw excellent agreement.
On the right plot (made with maptlotlib), there are actually multiple contours
overlaid, not just one with cross-hatching, but the agreement between the C++ results and pyhf
is so good it is very difficult to see any deviations.
As an additional really nice aspect, when we computed all the points required to construct
this contour `pyhf` was able to do so significantly faster
--- taking minutes as compared to hours!

## Slide 15

The publication of the full likelihoods to HEPData using the pyhf schema has an
additional distinction of solving a nearly 20 year old problem in the field of
particle physics.

At a workshop in 2000, whose proceedings the quotes here are taken from, there was agreement in the community that the LHC experiments should publish their likelihoods as part of the
results.
However, the technical aspect of what exactly to publish and how are non-trivial.
By focusing on just HistFactory models given their extensive use, we were able to make good on this agreement
when in 2019 the ATLAS collaboration published to HEPData the likelihoods
for a search for
bottom-squark pair production in final states containing Higgs bosons, b-jets and missing transverse momentum.

## Slide 16

The speedups we observed with `pyhf` on a single machine can be further improved by
parallelizing the fits of all the signal hypotheses.
Here we see a GIF of a Jupyter notebook that is sending out fits of the models
for all the signal hypotheses
to run on 25 worker nodes in the cloud
and then updating the exclusion contour plot in realtime as the fit results come in.

As the different fits are independent of each other the patched background and signal
models can be sent out to worker nodes on demand, taking advantage of this scaling
to make quick work of this embarrassingly parallelizable problem.
Through this weak parallelism
the same contour plot we just saw can be fully reproduced in just 3 minutes.
This clearly motivates the idea of "fitting as a service" on clusters in the future.

## Slide 17

The reason for `pyhfs` performance comes from the choice to use tensor algebra libraries
as our computational backends.
Our default backend, as you may have noticed from the examples so far, is NumPy with
SciPy providing the optimizer.
We additionally also support PyTorch, TensorFlow, and JAX as computational
backends with full feature parity.

One of the motivations for choosing machine learning frameworks as backends is to
exploit automatic differentation of their computational graphs and the hardware
acceleration on GPUS they are designed to work with to speedup fits.
As can be seen in the lower left plot, in this preliminary study of the effects of hardware acceleration
on pyhf fit times for, admittedly somewhat unrealistic models, we see that as the
model complexity grows there is significant gains in the speedups provided by GPUs.
In some cases even an order of magnitude.
This has allowed for some real models to move from being fit in hours to minutes and
minutes to seconds --- turning overnight jobs into nearly interactive analyses
(or at least an excuse to go for a coffee).

Additionally, while we like to think good things about ourselves, physicists are
not professional software engineers or the incredible NumPy dev team.
We're physicists. So being able to build on top of the hard work of the professionals
that build these open source libraries is hugely empowering.

## Slide 18

What `pyhf` provides is an unified API to our computational backends through our `tensorlib` shim.

You can see here for our four supported backends the code needed for pyhf to provide
a Normal distribution object through our `tensorlib.normal_dist` API,
without the analyst ever needing to care which backend they've chosen to use.

## Slide 19

This additionally allows for transparently changing the backend with our `set_backend` API.
In this example, we see that using `pyhf`s API we are able to build two Normal distributions
and then evaluate their `logpdf` for particular observation values in the
native tensor representation of each backend. All of course giving consistent values.

## Slide 20

Additionally, for the tensor library backends that provide automatic differentiation
we gain access to the full gradient of the likelihood resulting in our accuracy being limited
by floating point precision.

We can exploit the full gradient by providing it to the modern optimizers our backends provide
to help speedup the fit.

It is also worth pointing out that this is made possible by the fact that the backends are
constructing computational graphs for our model, as we saw before, and then applying the
chain rule to the tensorized operations in these graphs to move the gradients through the
graphs along with the data.

The benefits that are received from these tensorized representations
are not to be understated.
The ability to represent the HistFactory models in the graphs visually alone is impressive

## Slide 21

Where for comparison, this is the graph of the model used in the Higgs discovery in the `C++`
framework. Zooming out to have it all fit on screen makes it difficult to even see the nodes
of the operations.
I think this serves as a good visual example of the wins that we get from moving computational complexity
into tensor dimensionality.

## Slide 22

`pyhf` is already staring to be used in physics publications in the high energy physics
community.
What is exciting is that both theorists and experimenalists are using it.
On the left, you can see a phenomenology paper that used `pyhf` for performing reinterpretation,
with the GIF below cycling through models,
and on the right you can see the public note that ATLAS released on the use of public full likelihoods
for reproduction of results.
Below that is the CERN news article that was published on open full likelihoods,
highlighting what a dramatic change it had allowed.

## Slide 23

We'd also like to think that the uses of `pyhf` are not only found inside of high energy
physics.
Here we see public data from the Fermi Large Area Telescope analyzed with pyhf in a Jupyter notebook.
The LAT is a high energy gamma-ray telescope on the
Fermi Gamma Ray Space Telescope spacecraft used to observed gamma-ray photons coming
from extreme cosmological events.

We can represent the photon counts in the LAT as a binned model, such that after
constructing a model in pyhf and performing a maximum likelihood fit the
results can be visualized with healphy.
Here we can view the resulting mapping as a two dimensional histogram with
special binning choices.

While none of the pyhf core dev team works in astrophysics, we're interested to see
what overlaps might exist for use of `pyhf`.

## Slide 24

In summary, `pyhf` is a statistical library that provides
accelerated fitting for high energy physics models by exploiting
tensor libraries as computational backends for vectorized operations, automatic differentiation, and hardware acceleration.

It uses a JSON schema to provide a flexible specification for declarative models
and through JSON patch is an enabling technology for reinterpretation of physics results.

pyhf is also at the heart of the growing Pythonic ecosystem in high energy physics.
So let me plug the talks of my Scikit-HEP and IRIS-HEP colleagues, Jim and Henry, who are both
giving talks in this week in the High Performance Python track --- go check them
out as they're going to be great!
Also feel free to ask use any questions about Scikit-HEP or IRIS-HEP!

## Slide 25

Thank you so much for listening to my talk!
Here I'll note that pyhf is a Scikit-HEP project and I receive support from IRIS-HEP to develop it.

I've been so excited to get to talk with you at SciPy this year and I can say
on behalf of Lukas, Giordon, and me that we would love to get to talk with you more
about `pyhf`.
So please come talk to us and I'm looking forward to the Q&A tomorrow!

## Outro

Finally, I want to thank the SciPy organizers for all that they did this year
to make this conference happen and make it a success.
You've done a heroic job and I want to say thank you for giving me an opportunity
to share our work here with everyone.
