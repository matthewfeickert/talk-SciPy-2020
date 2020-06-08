class: middle, center, title-slide
count: false

# pyhf
.large[a pure Python statistical fitting library with tensors and autograd]

.center.width-30[[![pyhf_logo](https://iris-hep.org/assets/logos/pyhf-logo.png)](https://github.com/scikit-hep/pyhf)]<br><br>
.huge.blue[Matthew Feickert]<br>
<br>
[matthew.feickert@cern.ch](mailto:matthew.feickert@cern.ch)<br>
[@HEPfeickert](https://twitter.com/HEPfeickert)

[SciPy 2020](https://talk-event-url)

July 7th, 2020

---
# Self notes while writing talk

- Ensure that your talk will be relevant to a broad range of people. If your talk is on a particular Python package or piece of software, it should useful to more than a niche group.
- Include links to source code, articles, blog posts, or other writing that adds context to the presentation.
- If you've given a talk, tutorial, or other presentation before, include that information as well as a link to slides or a video if they're available.
- .bold[SciPy talks are generally 25 minutes] with 2-3 minutes for questions. Please keep the length of time in mind as you structure your outline.
- Your talk should not be a commercial for your company’s product. However, you are welcome to talk about how your company solved a problem, or notable open-source projects that may benefit attendees.
- .bold[NONE OF THESE PEOPLE KNOW WHAT PARTICLE PHYSICS IS]
   - Remove usage of "Standard Model" or BSM

---
class: middle

# Introduction and Motivation

Remove this later

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

.center[.bold[This is a _mathematical_ representation!] Nowhere is any software spec defined]

Basic structure: simultaneous fit to

- .blue[multiple "channels"] (analysis regions, (stacks of) histograms)
- each region can have .blue[multiple bins]
- coupled to a set of .red[constraint terms]

.center[.bold[Until now], the only implementation of HistFactory has been in a monolithic `C++` library used in HEP (`ROOT`)]

.bold[Challenges]
- Preservation: Likelihood stored in a domain specific binary format
   - Challenge for long-term preservation
- To start using HistFactory p.d.f.s first have to learn a whole `C++` framework
- Difficult to use for reinterpretation

---
# Example pyhf JSON spec

.center[<a href="https://carbon.now.sh/?bg=rgba(255%2C255%2C255%2C1)&t=seti&wt=none&l=application%2Fjson&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=true&pv=3px&ph=1px&ln=false&fl=1&fm=Hack&fs=14px&lh=133%25&si=false&es=4x&wm=false&code=%257B%250A%2520%2520%2520%2520%2522channels%2522%253A%2520%255B%2520%2523%2520List%2520of%2520regions%250A%2520%2520%2520%2520%2520%2520%2520%2520%257B%2520%2522name%2522%253A%2520%2522singlechannel%2522%252C%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2522samples%2522%253A%2520%255B%2520%2523%2520List%2520of%2520samples%2520in%2520region%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%257B%2520%2522name%2522%253A%2520%2522signal%2522%252C%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2522data%2522%253A%2520%255B5.0%252C%252010.0%255D%252C%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2523%2520List%2520of%2520rate%2520factors%2520and%252For%2520systematic%2520uncertainties%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2522modifiers%2522%253A%2520%255B%2520%257B%2520%2522name%2522%253A%2520%2522mu%2522%252C%2520%2522type%2522%253A%2520%2522normfactor%2522%252C%2520%2522data%2522%253A%2520null%257D%2520%255D%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%257D%252C%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%257B%2520%2522name%2522%253A%2520%2522background%2522%252C%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2522data%2522%253A%2520%255B50.0%252C%252060.0%255D%252C%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2522modifiers%2522%253A%2520%255B%2520%257B%2522name%2522%253A%2520%2522uncorr_bkguncrt%2522%252C%2520%2522type%2522%253A%2520%2522shapesys%2522%252C%2520%2522data%2522%253A%2520%255B5.0%252C%252012.0%255D%257D%2520%255D%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%257D%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%255D%250A%2520%2520%2520%2520%2520%2520%2520%2520%257D%250A%2520%2520%2520%2520%255D%252C%250A%2520%2520%2520%2520%2522observations%2522%253A%2520%255B%2520%2523%2520Observed%2520data%250A%2520%2520%2520%2520%2520%2520%2520%2520%257B%2520%2522name%2522%253A%2520%2522singlechannel%2522%252C%2520%2522data%2522%253A%2520%255B50.0%252C%252060.0%255D%2520%257D%250A%2520%2520%2520%2520%255D%252C%250A%2520%2520%2520%2520%2522measurements%2522%253A%2520%255B%2520%2523%2520Parameter%2520of%2520interest%250A%2520%2520%2520%2520%2520%2520%2520%2520%257B%2520%2522name%2522%253A%2520%2522Measurement%2522%252C%2520%2522config%2522%253A%2520%257B%2522poi%2522%253A%2520%2522mu%2522%252C%2520%2522parameters%2522%253A%2520%255B%255D%257D%2520%257D%250A%2520%2520%2520%2520%255D%252C%250A%2520%2520%2520%2520%2522version%2522%253A%2520%25221.0.0%2522%2520%2523%2520Version%2520of%2520spec%2520standard%250A%257D">`JSON` defining a single channel, two bin counting experiment with systematics</a>]

.center.width-80[![demo_JSON](figures/carbon_JSON_spec_annotated.png)]

---
class: middle

# Performance gain through tensorization

Remove this later

---
# Performance seciton notes

- From watching the [`Freud` SciPy 2019 talk](https://youtu.be/D0LWh1BzPRQ) it is probably totally fine to show much more detailed examples of what is actually happening with the shim layers

---
# Machine Learning Frameworks for Computation

.grid[
.kol-2-3[
- All numerical operations implemented in .bold[tensor backends] through an API of $n$-dimensional array operations
- Using deep learning frameworks as computational backends allows for .bold[exploitation of auto differentiation (autograd) and GPU acceleration]
- As huge buy in from industry we benefit for free as these frameworks are .bold[continually improved] by professional software engineers

.kol-1-2.center[
.width-90[![scaling_hardware](figures/scaling_hardware_annotated.png)]
]
.kol-1-2[
- Preliminary results
- Show hardware acceleration giving .bold[order of magnitude speedup] for some models!
- Hardware acceleration benchmarking planned
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
# Unified API through shim tensorlib
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
class: middle

# Model specification

Remove this later

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
# Likelihood serialization and reproduction
<!--  -->
- ATLAS note on the JSON schema for serialization and reproduction of results [[ATL-PHYS-PUB-2019-029](https://cds.cern.ch/record/2684863)]
   - Contours: .root[█] original ROOT+XML, .pyhf[█] pyhf JSON, .roundtrip[█] JSON converted back to ROOT+XML
      - Overlay of expected limit **contours** (hatching) and observed **lines** nice visualization of near perfect agreement
   - Serialized likelihood and reproduced results of ATLAS Run-2 search for sbottom quarks [[JHEP12(2019)060](http://inspirehep.net/record/1748602)] and published to HEPData
   - Shown to reproduce results but faster! .bold[ROOT:] 10+ hours .bold[pyhf:] < 30 minutes

.kol-1-2.center.width-95[
[![overlay_multiplex_contour](figures/overlay_multiplex_contour.png)](https://cds.cern.ch/record/2684863)
]
.kol-1-2.right.width-70[
[![discrepancy](figures/discrepancy.png)](https://cds.cern.ch/record/2684863)
]

---
# Publications using pyhf

.kol-1-2.center.width-95[
.center.width-70[[![arxViv_header](figures/arXiv_1810-05648_header.png)](https://inspirehep.net/record/1698425)]

.center.width-40[[![arxViv_tweet_GIF](figures/pyhf_arXiv.gif)](https://twitter.com/lukasheinrich_/status/1052142936803160065)]
]
.kol-1-2.center.width-95[
.center.width-100[[![ATLAS_PUB_Note_title](figures/ATLAS_PUB_Note_title.png)](https://cds.cern.ch/record/2684863)]

.center.width-100[[![CERN_news_story](figures/CERN_news_story.png)](https://home.cern/news/news/knowledge-sharing/new-open-release-allows-theorists-explore-lhc-data-new-way)]
]

---
class: middle

# Conclusions

Remove this later

---
# Summary
.kol-1-2[
.large[`pyhf` provides:]
- .large[Accelerated fitting]
   - .bold[reducing time to insight]!
   - Hardware acceleration on GPUs and vectorized operations
   - Backend agnostic acceleration
   - Human acceleration through clean Pythonic API
- .large[Flexible schema great for open likelihood .bold[preservation]]
   - JSON: ubiquitous, universal support, versionable
   - Easily describe HistFactory models
   - First full likelihood from an LHC experiment openly published
- .large[Enabling technology for .bold[reinterpretation]]
   - JSON Patch files for efficient computation of new signal models
]
.kol-1-2[
<br>
<br>
<br>
.center.width-60[[![pyhf_logo](https://iris-hep.org/assets/logos/pyhf-logo.png)](https://github.com/scikit-hep/pyhf)]
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
