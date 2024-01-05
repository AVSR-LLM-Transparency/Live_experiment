## Live Experiment
The newly integrated ROS Module, ”Live experiment,” introduces two key functionalities.
The first is to facilitate interaction with users during experiments, providing responses
and guidance. The second functionality involves the preservation of critical experimental
data that we are focusing on. This module operates almost parallelly with the system’s
original State Flow, implying minimal major alterations to the core structure. Instead, it
activates the ’Live experiment’ operations upon reaching certain states within the existing
system. 

The figure below vividly illustrates the updated state flow transitions. These are
differentiated by three colors representing three distinct sections. **Black** denotes the
original state transition flow of the system. **The blue section** highlights the triggering
of different stages of the ’Live experiment’ and their corresponding relationships with the
original system. This is further categorized into user interaction and data preservation
operations. **The orange section** shows five types of data saved by the ‘Live experiment’:
three durations, the results of AVSR, and the response from the LLM. It’s noteworthy
that Our Local Pipeline’s LLM response is provided to the user word by word, hence
the inclusion of a state called ’LLM 1st word’. Additionally, throughout various stages
of the live experiment, especially during waiting periods, users will receive interactive
information from the system to ensure a user-friendly process experience.



![updated State Flow](https://github.com/AVSR-LLM-Transparency/Live_experiment/blob/17f1127cb9bb450ca1d0755e74ce558eeb719587/updated%20State%20Flow.png)
