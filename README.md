# MANIFEST: a huMAN-centric explaInable approach for FakE news Spreading deTection

Fake news spreading is an ever increasing phenomenon which is deeply tied with the involvement of humans as they tend to adopt, circulate and fall for misinformation stories. However, there has not been significant work in the literature on the role that the human factor has and what characteristics of human users correlate with the diffusion of fake news. Such research would be valuable to better understand and combat misinformation patterns in human dominated platforms such as social networks. Recent work has shown that behavioral user profiling leads to promising results in identifying fake news spreaders. In spite of this, no in-depth analysis has been made to figure out the exact features that correlate with fake news spreading behavior. This work suggests an explainable human-centric approach on detecting fake news spreading behavior by building a fake news spreader classifier, utilizing the psychological characteristics of human users and applying state of the art explanation techniques. Experimentation demonstrates that our model achieves promising results at detecting fake news spreaders by utilizing user characteristics while also offering explanations of which of those characteristics contribute to the fake news spreading behavior. 

In addition, to the best of our knowledge, this is the first work that aims to provide a fully explainable setup that evaluates fake news spreading based on users credibility applied to public discussions on Twitter threads and aiming for a comprehensive way to combat fake news circulation. The way we approach this is by utilizing the predictions made by the fake news spreader classifier built before on the users that took part in the discussion of a specific twitter thread and then by learning an interpretable linear model in that space. The explanations consist of example-based explanations and word feature importance. Quantitative evaluation shows that the linear model is able to accurately imitate the predictions of the more complex fake news spreader classifier with a high accuracy. Qualitative evaluation shows that the explanations are reasonable and intuitive and could prove fruitful for combating the propagation of fake news.

## Comments

For the fake news spreader dataset please request it via Zenodo [here](https://zenodo.org/record/3692319#.YFs3CK8zZPY) and afterwards put the data in a new directory called data inside the dataset folder.

## References

F. Rangel, P. Rosso, B. Ghanem, A. Giachanou. [Profiling Fake News Spreaders on Twitter](https://zenodo.org/record/4039435#.YFHgv50zZPZ). Zenodo, February 2020

D. Karanatsiou, P. Sermpezis, J. Gruda, K. Kafetsios, I. Dimitriadis, A. Vakali. [My tweets bring all the traits to the yard: Predicting personality and relational traits in Online Social Networks](https://arxiv.org/abs/2009.10802). arXiv preprint arXiv:2009.10802 (2020).
