class: middle, center, title-slide
count: false

# pyhf
.large[a pure Python statistical fitting library with tensors and autograd]

.center.width-30[[![pyhf_logo](https://iris-hep.org/assets/logos/pyhf-logo.png)](https://github.com/scikit-hep/pyhf)]<br><br>
.huge.blue[Matthew Feickert]<br>

<!-- Provided by fontawesome under the Creative Commons Attribution 4.0 International license https://fontawesome.com/license -->
.width-02[![email](figures/email.svg)] [matthew.feickert@cern.ch](mailto:matthew.feickert@cern.ch)<br>
.width-02[![Twitter](figures/twitter.svg)] [@HEPfeickert](https://twitter.com/HEPfeickert)<br>
.width-02[![GitHub](figures/github.svg)] [matthewfeickert](https://github.com/matthewfeickert)

[SciPy 2020](https://talk-event-url)<br>
July 7th, 2020

---
# Self notes while writing talk

- Ensure that your talk will be relevant to a broad range of people. If your talk is on a particular Python package or piece of software, it should useful to more than a niche group.
- Include links to source code, articles, blog posts, or other writing that adds context to the presentation.
- If you've given a talk, tutorial, or other presentation before, include that information as well as a link to slides or a video if they're available.
- .bold[SciPy talks are generally 25 minutes] with 2-3 minutes for questions. Please keep the length of time in mind as you structure your outline.
- Your talk should not be a commercial for your company’s product. However, you are welcome to talk about how your company solved a problem, or notable open-source projects that may benefit attendees.
- .bold[NONE OF THESE PEOPLE KNOW WHAT PARTICLE PHYSICS IS]
- Accepted abstract is here: https://github.com/matthewfeickert/SciPy2020-Proposal
   - Use abstract as outline
- [In general track](https://na.eventscloud.com/ehome/487022?&t=d2917a15274e1daf79d80a4253f01e7a)...so think about how this talk will align

---
# `pyhf` core dev team

<br>

.grid[
.kol-1-3.center[
.circle.width-80[![Lukas](figures/collaborators/heinrich.jpg)]

[Lukas Heinrich](https://github.com/lukasheinrich)

CERN
]
.kol-1-3.center[
.circle.width-80[![Matthew](https://avatars2.githubusercontent.com/u/5142394)]

[Matthew Feickert](https://www.matthewfeickert.com/)

Illinois
]
.kol-1-3.center[
.circle.width-75[![Giordon](https://avatars0.githubusercontent.com/u/761483)]

[Giordon Stark](https://github.com/kratsg)

UCSC SCIPP
]
]

---
# We're high energy particle physicists
.kol-1-2.center[
<br>
.width-95[[![LHC](figures/LHC.jpg)](https://home.cern/science/accelerators/large-hadron-collider)]
LHC
]
.kol-1-2.center[
.width-95[[![ATLAS_TRex](figures/ATLAS_TRex.png)](https://atlas.cern/)]
ATLAS
]
.kol-1-1[
.kol-1-2.center[
.width-45[[![SM_mug](figures/SM_mug.jpg)](https://twitter.com/HEPfeickert/status/1269406145858469891?s=20)]
]
.kol-1-2.center[
.kol-1-2.center[
.width-100[[![ParticleZoo_Higgs](figures/ParticleZoo_Higgs.jpg)](https://twitter.com/HEPfeickert/status/1269406145858469891?s=20)]
]
.kol-1-2.center[
.width-85[[![ParticleZoo_DarkMatter](figures/ParticleZoo_DarkMatter.jpg)](https://twitter.com/HEPfeickert/status/1269406145858469891?s=20)]
]
]
]

---
# So we want to know

<br>
.center.width-100[[![CERN_ribbon_of_truth](figures/CERN_ribbon_of_truth.png)](https://home.cern/)]

---
# Goals of physics analysis at the LHC

.kol-1-1[
.kol-1-3.center[
.width-100[[![ATLAS_Higgs_discovery](figures/ATLAS_Higgs_discovery.png)](https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/HIGG-2012-27/)]
Search for new physics
]
.kol-1-3.center[
<br>
.width-100[[![CMS-PAS-HIG-19-004](figures/CMS-PAS-HIG-19-004.png)](http://cms-results.web.cern.ch/cms-results/public-results/superseded/HIG-19-004/index.html)]

<br>
Make precision measurements
]
.kol-1-3.center[
.width-110[[![SUSY-2018-31_limit](figures/SUSY-2018-31_limit.png)](https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/SUSY-2018-31/)]

Provide constraints on models through setting best limits
]
]

- All require .bold[building statistical models] and .bold[fitting models] to data to perform statistical inference
- Model complexity can be huge for complicated searches
- **Problem:** Time to fit can be .bold[many hours]
- .blue[Goal:] Empower analysts with fast fits and expressive models

---
# HistFactory Model

- A flexible probability density function (p.d.f.) template to build binned statistical models
- Developed during work that lead to the Higgs discovery in 2011 [[CERN-OPEN-2012-016](http://inspirehep.net/record/1236448)]
- Widely used by the high energy physics (HEP) community for .bold[measurements of known physics] (Standard Model) and .bold[searches for new physics] (beyond the Standard Model)

.kol-2-8.center[
<br>
.width-100[[![HIGG-2016-25](figures/HIGG-2016-25.png)](https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/HIGG-2016-25/)]
<br>
.bold[Standard Model]
]
.kol-3-8.center[
<br>
.width-100[[![SUSY-2016-16](figures/SUSY-2016-16.png)](https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/SUSY-2016-16/)]
<br>
<br>
.bold[Supersymmetry]
]
.kol-3-8.center[
<br>
.width-100[[![EXOT-2016-25](figures/EXOT-2016-25.png)](https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/EXOT-2016-25/)]
<br>
.bold[Exotic Physics]
]

---
# HistFactory Template

$$
f\left(\vec{n}, \vec{a}\middle|\vec{\eta}, \vec{\chi}\right) = \color{blue}{\prod\_{c \\,\in\\, \textrm{channels}} \prod\_{b \\,\in\\, \textrm{bins}\_c} \textrm{Pois} \left(n\_{cb} \middle| \nu\_{cb}\left(\vec{\eta}, \vec{\chi}\right)\right)} \\,\color{red}{\prod\_{\chi \\,\in\\, \vec{\chi}} c\_{\chi} \left(a\_{\chi}\middle|\chi\right)}
$$

$$
\nu\_{cb}(\vec{\eta}, \vec{\chi}) = \sum\_{s \\,\in\\, \textrm{samples}} \underbrace{\left(\sum\_{\kappa \\,\in\\, \vec{\kappa}} \kappa\_{scb}(\vec{\eta}, \vec{\chi})\right)}\_{\textrm{multiplicative}} \Bigg(\nu\_{scb}^{0}(\vec{\eta}, \vec{\chi}) + \underbrace{\sum\_{\Delta \\,\in\\, \vec{\Delta}} \Delta\_{scb}(\vec{\eta}, \vec{\chi})}\_{\textrm{additive}}\Bigg)
$$

.bold[Use:] Multiple disjoint _channels_ (or regions) of binned distributions with multiple _samples_ contributing to each with additional (possibly shared) systematics between sample estimates

.bold[Main pieces:]
- .blue[Main Poisson p.d.f. for simultaneous measurement of multiple channels]
- .katex[Event rates] $\nu\_{cb}$ from nominal rate $\nu\_{scb}^{0}$ and rate modifiers $\kappa$ and $\Delta$
- .red[Constraint p.d.f. (+ data) for "auxiliary measurements"]
   - encoding systematic uncertainties (normalization, shape, etc)
- $\vec{n}$: events, $\vec{a}$: auxiliary data, $\vec{\eta}$: unconstrained pars, $\vec{\chi}$: constrained pars

---
# HistFactory Template

$$
f\left(\vec{n}, \vec{a}\middle|\vec{\eta}, \vec{\chi}\right) = \color{blue}{\prod\_{c \\,\in\\, \textrm{channels}} \prod\_{b \\,\in\\, \textrm{bins}\_c} \textrm{Pois} \left(n\_{cb} \middle| \nu\_{cb}\left(\vec{\eta}, \vec{\chi}\right)\right)} \\,\color{red}{\prod\_{\chi \\,\in\\, \vec{\chi}} c\_{\chi} \left(a\_{\chi}\middle|\chi\right)}
$$

Basic structure: simultaneous fit to

- .blue[multiple "channels"] (analysis regions, (stacks of) histograms)
- each region can have .blue[multiple bins]
- coupled to a set of .red[constraint terms]

.center[.bold[This is a _mathematical_ representation!] Nowhere is any software spec defined]
.center[.bold[Until now] (2018), the only implementation of HistFactory has been in a monolithic `C++` library used in HEP (`ROOT`)]

.bold[`pyhf`: HistFactory in pure Python]
.center.width-70[[![pyhf_PyPI](figures/pyhf_PyPI.png)](https://pypi.org/project/pyhf/)]

---
# Basic object of HistFactory is the statistical model

$$
f\left(\vec{n}, \vec{a}\middle|\vec{\eta}, \vec{\chi}\right) = \prod\_{c \\,\in\\, \textrm{channels}} \prod\_{b \\,\in\\, \textrm{bins}\_c} \textrm{Pois} \left(n\_{cb} \middle| \nu\_{cb}\left(\vec{\eta}, \vec{\chi}\right)\right) \prod\_{\chi \\,\in\\, \vec{\chi}} c\_{\chi} \left(a\_{\chi}\middle|\chi\right)
$$

.center[care about log likelihood as using maximum likelihood fits]

$$
\ln L \left(\vec{\theta} \\,\middle| \vec{x}\right) \Rightarrow \texttt{model.logpdf(parameters, data)}
$$

.center.width-100[![carbon_logpdf_example.png](figures/carbon_logpdf_example.png)]

---
# Model is represented as a computational graph
.grid[
.kol-1-3[
<br>
- Each node of the graph represents a vectorized n-dimensional array ("tensorized") operation
- The graph (model) is largely factorized between the .pars_blue[parameter] graph and the .data_green[data] graph
- The bottom node is the final log likelihood .value_orange[value]
<br>
<br>
$$
\texttt{\textcolor{#ddc16c}{value} = model.logpdf(\textcolor{#73bbe6}{parameters}, \textcolor{#a5dc92}{data})}
$$
]
.kol-2-3[
.center.width-90[![DAG](figures/computational_graph.png)]
]
]

---
# Core task: Maximum likelihood fits

$$
\texttt{pyhf.infer.mle.fit(data, model)}
$$

.center[minimizes the objective function $-2\ln L \left(\vec{\theta} \\,\middle| \vec{x}\right)$ (maximizing the likelihood) with the backend's optimizer]
<br>

.center.width-100[![carbon_mle_fit_example](figures/carbon_mle_fit_example.png)]

---
# Use in profile likelihood fits (thing we care about)
$$
-2\ln \Lambda (\mu) = - 2\ln\frac{L(\mu, \hat{\\!\hat{\theta}})}{L(\hat{\mu}, \hat{\theta})} \quad \frac{\Leftarrow\textrm{constrained best fit}}{\Leftarrow\textrm{unconstrained best fit}}
$$
<!--  -->
to compute a modified $p$-value called the $\mathrm{CL}_{s}$ for a given parameter of interest $\mu$ &mdash; hypothesis testing!
$$
\texttt{pyhf.infer.hypotest(testpoi, data, model)}
$$
<!--  -->
.center[Want this .bold[fast as possible!]]
<!--  -->
.center.width-70[![carbon_hypotest_example](figures/carbon_hypotest_example.png)]

---
# JSON spec fully describes the HistFactory model

.kol-1-4.width-100[
- Human & machine readable
- Industry standard
   - Will be with us forever
- Parsable by every language
   - Highly portable
   - No lock in
- Versionable and easily preserved
   - JSON Schema [describing<br> HistFactory specification](https://scikit-hep.org/pyhf/likelihood.html#bibliography)
   - Attractive for analysis preservation
   - Highly compressible
]
.kol-3-4.center[
.width-105[![demo_JSON](figures/carbon_JSON_spec_annotated.png)]

.center[[`JSON` defining a single channel, two bin counting experiment with systematics](https://scikit-hep.org/pyhf/likelihood.html#toy-example)]
]

---
# JSON Patch for signal model (reinterpretation)
<!--  -->
.center[JSON Patch gives ability to .bold[swap signal models]!]
.center[Allows for .bold[separating] the background model from the signal model]
.center[(think scans in parameter space)]
<!--  -->
.kol-1-5[
<br>
<br>
<br>
<br>
.center.width-100[![measurement_cartoon](figures/measurement_cartoon.png)]
.center[Signal model A]
]
.kol-3-5[
<!-- Using Perl style in Carbon -->
.center.width-100[![signal_reinterpretation](figures/carbon_reinterpretation.png)]
]
.kol-1-5[
<br>
<br>
<br>
<br>
.center.width-100[![reinterpretation_cartoon](figures/reinterpretation_cartoon.png)]
.center[Signal model B]
]

---
# Allows for analysis preservation and reuse

- Background-only model JSON stored
- Hundreds of signal model JSON Patches stored together as a "patch set" file
- Together are able to fully preserve the full model (with own DOI! .width-20[[![DOI](https://img.shields.io/badge/DOI-10.17182%2Fhepdata.90607.v2%2Fr2-blue.svg)](https://doi.org/10.17182/hepdata.90607.v2/r2)] )

[.center.width-70[![HEPData_likelihoods](figures/HEPData_likelihoods.png)]](https://www.hepdata.net/record/ins1748602)

---
# Likelihood serialization and reproduction
<!--  -->
- ATLAS note on the JSON schema for serialization and reproduction of results [[ATL-PHYS-PUB-2019-029](https://cds.cern.ch/record/2684863)]
   - Contours: .root[█] original ROOT+XML, .pyhf[█] pyhf JSON, .roundtrip[█] JSON converted back to ROOT+XML
      - Overlay of expected limit **contours** (hatching) and observed **lines** nice visualization of near perfect agreement
   - Serialized likelihood and reproduced results of ATLAS Run-2 search for bottom-squarks [[JHEP12(2019)060](http://inspirehep.net/record/1748602)] and published to HEPData
   - Shown to reproduce results but faster! .bold[C++ (ROOT):] 10+ hours .bold[pyhf:] < 30 minutes

.kol-1-2.center.width-95[
[![overlay_multiplex_contour](figures/overlay_multiplex_contour.png)](https://cds.cern.ch/record/2684863)
]
.kol-1-2.right.width-70[
[![discrepancy](figures/discrepancy.png)](https://cds.cern.ch/record/2684863)
]

---
# Further speed up by parallelizing across cluster

.kol-1-3[
<br>
- Running across 25 worker nodes on the cloud
- Background and signal patches are sent to workers on demand
   - Possible as the signal patches don't need information from each other
   - Embarrassingly parallelizable
- Results being plotted as they are streamed back
- Fit of same likelihood now takes .bold[3 minutes] for all signal points!
]
.kol-2-3[
<!-- https://github.com/lukasheinrich/lhoodbinder2 -->
<!-- .center.width-45[[![plot_countour](plot_countour.gif)](http://www.cern.ch/feickert/talks/plot_countour.gif)] -->
.center.width-70[[![plot_countour](http://www.cern.ch/feickert/talks/plot_countour.gif)](http://www.cern.ch/feickert/talks/plot_countour.gif)]
.center.small[(GIF sped up by 8x)]
]

---
# Machine Learning Frameworks for Computation

.grid[
.kol-2-3[
- All numerical operations implemented in .bold[tensor backends] through an API of $n$-dimensional array operations
- Using deep learning frameworks as computational backends allows for .bold[exploitation of auto differentiation (autograd) and GPU acceleration]
- As huge buy in from industry we benefit for free as these frameworks are .bold[continually improved] by professional software engineers (physicists are not)

.kol-1-2.center[
.width-90[![scaling_hardware](figures/scaling_hardware_annotated.png)]
]
.kol-1-2[
<br>
- Show hardware acceleration giving .bold[order of magnitude speedup] for some models!
- Improvements over traditional
   - 10 hrs to 30 min; 20 min to 10 sec
]
]
.kol-1-4.center[
.width-85[![NumPy](figures/logos/NumPy_logo.svg)]
.width-85[![PyTorch](figures/logos/Pytorch_logo.svg)]
.width-85[![Tensorflow](figures/logos/TensorFlow_logo.svg)]

<br>
.width-50[![JAX](figures/logos/JAX_logo.png)]
]
]

---
# Unified API through `tensorlib` shim
<!--  -->
.kol-1-1[
.kol-1-2.center[
.width-90[[![carbon_normal_dist_numpy](figures/carbon_normal_dist_numpy.png)](https://scikit-hep.org/pyhf/_generated/pyhf.tensor.numpy_backend.numpy_backend.html#pyhf.tensor.numpy_backend.numpy_backend.normal_dist)]

NumPy
]
.kol-1-2.center[
.width-90[[![carbon_normal_dist_jax](figures/carbon_normal_dist_jax.png)](https://scikit-hep.org/pyhf/_generated/pyhf.tensor.jax_backend.jax_backend.html#pyhf.tensor.jax_backend.jax_backend.normal_dist)]
<br>JAX
]
]
.kol-1-1[
.kol-1-2.center[
.width-95[[![carbon_normal_dist_tensorflow](figures/carbon_normal_dist_tensorflow.png)](https://scikit-hep.org/pyhf/_generated/pyhf.tensor.tensorflow_backend.tensorflow_backend.html#pyhf.tensor.tensorflow_backend.tensorflow_backend.normal_dist)]
<br>Tensorflow
]
.kol-1-2.center[
.width-95[[![carbon_normal_dist_pytorch](figures/carbon_normal_dist_pytorch.png)](https://scikit-hep.org/pyhf/_generated/pyhf.tensor.pytorch_backend.pytorch_backend.html#pyhf.tensor.pytorch_backend.pytorch_backend.normal_dist)]
<br>PyTorch
]
]

---
# Allows for transparently changing backend

.center.width-100[![carbon_change_backend](figures/carbon_change_backend.png)]

---
# Automatic differentiation

With tensor library backends gain access to _exact (higher order) derivatives_ &mdash; accuracy is only limited by floating point precision

$$
\frac{\partial L}{\partial \mu}, \frac{\partial L}{\partial \theta_{i}}
$$

.grid[
.kol-1-2[
.large[Exploit .bold[full gradient of the likelihood] with .bold[modern optimizers] to help speedup fit!]

<br><br>
.large[Gain this through the frameworks creating _computational directed acyclic graphs_ and then applying the chain rule (to the operations)]
]
.kol-1-2[
.center.width-80[![DAG](figures/computational_graph.png)]
]
]

---
# Publications using `pyhf`

.kol-1-2.center.width-95[
.center.width-70[[![arxViv_header](figures/arXiv_1810-05648_header.png)](https://inspirehep.net/record/1698425)]

.center.width-40[[![arxViv_tweet_GIF](figures/pyhf_arXiv.gif)](https://twitter.com/lukasheinrich_/status/1052142936803160065)]
]
.kol-1-2.center.width-95[
.center.width-100[[![ATLAS_PUB_Note_title](figures/ATLAS_PUB_Note_title.png)](https://cds.cern.ch/record/2684863)]

.center.width-100[[![CERN_news_story](figures/CERN_news_story.png)](https://home.cern/news/news/knowledge-sharing/new-open-release-allows-theorists-explore-lhc-data-new-way)]
]

---
# Summary
.kol-2-3[
.large[`pyhf` provides:]
- .large[.bold[Accelerated] fitting library]
   - reducing time to insight/inference!
   - Hardware acceleration on GPUs and vectorized operations
   - Backend agnostic Python API and CLI
- .large[Flexible .bold[declarative] schema]
   - JSON: ubiquitous, universal support, versionable
- .large[Enabling technology for .bold[reinterpretation]]
   - JSON Patch files for efficient computation of new signal models
   - Unifying tool for theoretical and experimental physicists
- .large[Project in growing .bold[Pythonic HEP ecosystem]]
   - c.f. Jim Pivarski and Henry Schreiner's talks in High Performance Python track
   - Ask us about Scikit-HEP and PyHEP!
]
.kol-1-3[
<br>
<br>
<br>
.center.width-100[[![pyhf_logo](https://iris-hep.org/assets/logos/pyhf-logo.png)](https://github.com/scikit-hep/pyhf)]
]

---
class: middle

.center[
# Thanks for listening!
# Come talk with us!

.large[[www.scikit-hep.org/pyhf](https://scikit-hep.org/pyhf/)]
]
.grid[
.kol-1-3.center[
.width-90[[![scikit-hep_logo](https://scikit-hep.org/assets/images/logo.png)](https://scikit-hep.org/)]
]
.kol-1-3.center[
<br>
.width-90[[![pyhf_logo](https://iris-hep.org/assets/logos/pyhf-logo.png)](https://github.com/scikit-hep/pyhf)]
]
.kol-1-3.center[
<br>
<br>
.width-100[[![iris-hep_logo](figures/iris-hep-4-no-long-name.png)](https://iris-hep.org/)]
]
]


---
class: end-slide, center

Backup

---
# Why is the likelihood important?

<br>

.kol-1-2.width-90[
- High information-density summary of analysis
- Almost everything we do in the analysis ultimately affects the likelihood and is encapsulated in it
   - Trigger
   - Detector
   - Systematic Uncertainties
   - Event Selection
- Unique representation of the analysis to preserve
]
.kol-1-2.width-90[
<br><br><br>
[![likelihood_connections](figures/likelihood_connections.png)](https://indico.cern.ch/event/839382/contributions/3521168/)
]

---
# Likelihood serialization and reproduction
<!--  -->
- ATLAS note on the JSON schema for serialization and reproduction of results [[ATL-PHYS-PUB-2019-029](https://cds.cern.ch/record/2684863)]
   - Contours: .root[█] original ROOT+XML, .pyhf[█] pyhf JSON, .roundtrip[█] JSON converted back to ROOT+XML
<!--  -->
.right.width-80[
[![flowchart](figures/process.svg)](https://cds.cern.ch/record/2684863)
]

---
# References

1. F. James, Y. Perrin, L. Lyons, .italic[[Workshop on confidence limits: Proceedings](http://inspirehep.net/record/534129)], 2000.
2. ROOT collaboration, K. Cranmer, G. Lewis, L. Moneta, A. Shibata and W. Verkerke, .italic[[HistFactory: A tool for creating statistical models for use with RooFit and RooStats](http://inspirehep.net/record/1236448)], 2012.
3. L. Heinrich, H. Schulz, J. Turner and Y. Zhou, .italic[[Constraining $A_{4}$ Leptonic Flavour Model Parameters at Colliders and Beyond](https://inspirehep.net/record/1698425)], 2018.
4. A. Read, .italic[[Modified frequentist analysis of search results (the $\\mathrm{CL}_{s}$ method)](http://cds.cern.ch/record/451614)], 2000.
5. K. Cranmer, .italic[[CERN Latin-American School of High-Energy Physics: Statistics for Particle Physicists](https://indico.cern.ch/event/208901/contributions/1501047/)], 2013.
6. ATLAS collaboration, .italic[[Search for bottom-squark pair production with the ATLAS detector in final states containing Higgs bosons, b-jets and missing transverse momentum](http://inspirehep.net/record/1748602)], 2019
7. ATLAS collaboration, .italic[[Reproducing searches for new physics with the ATLAS experiment through publication of full statistical likelihoods](https://cds.cern.ch/record/2684863)], 2019
8. ATLAS collaboration, .italic[[Search for bottom-squark pair production with the ATLAS detector in final states containing Higgs bosons, b-jets and missing transverse momentum: HEPData entry](https://www.hepdata.net/record/ins1748602)], 2019

---

class: end-slide, center
count: false

The end.
