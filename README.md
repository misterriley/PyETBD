# PyETBD
Translation of McDowell's Evolutionary Theory of Behavior Dynamics from vbscript into python

This translation of vbscript to python has gotten rid of the original GUI due to difficulties in moving GUIs between the two languages. Rather, it is based on JSON files. 
You can find examples of these files in PyETBD/exp_files/. For more detail about the strucutre of these files see [JSON Structure.md](https://github.com/misterriley/PyETBD/blob/master/JSON%20Structure.md).

## Reference Information

The ETBD was created by [Dr. Jack McDowell](https://www.researchgate.net/profile/Jack-Mcdowell) as an instantiation of [B.F. Skinner's](https://en.wikipedia.org/wiki/B._F._Skinner) theory of [selection by consequences](https://scholar.google.com/scholar_url?url=https://discoversocialsciences.com/wp-content/uploads/2019/09/Skinner-selection-by-consequences.pdf&hl=en&sa=X&ei=B_aXYZrED8ySy9YP_K2EwAs&scisig=AAGBfm2KlvkxJBDs4vXx4SP17qEFrsalUw&oi=scholarr). It is a specialized type of [genetic algorithm](https://en.wikipedia.org/wiki/Genetic_algorithm). The ETBD has shown success in replicating patterns of behavior shown by humans and animals at several different timescales. For a thorough description of the algorithm and an overview of some of it's empirical outcomes see [McDowell (2019)](https://www.researchgate.net/publication/330469489_On_the_current_status_of_the_evolutionary_theory_of_behavior_dynamics_Status_of_the_Evolutionary_Theory).

The ETBD was recently extended to model punishment as well as reinforcement. See [McDowell and Klapes (2019)](https://onlinelibrary.wiley.com/doi/abs/10.1002/jeab.543?casa_token=8_8Obd8orrIAAAAA%3AuEZUYpifw4JIZARR7zeISfvoz4EtRa5dmaHV5FiNFG7ir4I8rICRIkUhsino1BRbNxIEiZF8I6lnums) for a description of how this was done and its empirical results. The version of the ETBD with punishment implemented is in the current (11/19/2021) version of PyETBD though it has not been tested thoroughly.   
