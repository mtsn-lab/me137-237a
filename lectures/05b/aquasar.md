<!-- image -->

<!-- image -->

Contents lists available at SciVerse ScienceDirect

## Energy

[journal homepage: www.elsevier.com/locate/energy](http://www.elsevier.com/locate/energy)

## Aquasar: A hot water cooled data center with direct energy reuse

Severin Zimmermann a,b , Ingmar Meijer b , Manish K. Tiwari a , Stephan Paredes b , Bruno Michel b , Dimos Poulikakos a, *

a Laboratory of Thermodynamics in Emerging Technologies, Mechanical and Process Engineering Department, ETH Zurich, 8092 Zurich, Switzerland b IBM Research Zurich, 8803 Rüschlikon, Switzerland

## article info

Article history: Received 1 February 2012 Received in revised form 11 April 2012 Accepted 12 April 2012 Available online 15 May 2012

Keywords: Electronic cooling Exergy Value of heat Hot water Cooling Energy reuse Green computing

## 1. Introduction

The rapidly growing demand for data processing in communication, education, finance and medicine calls for improved electronic components and it has resulted in ever increasing energy consumption by data centers [1]. Up to 50% of the consumed energy is spent to power the cooling infrastructure [2], thus making it a very important component in minimizing the energy consumption of a data center. A detailed study on a real air cooled data center performed by Mitchell-Jackson et al. [3] clarifies the fact of high power consumption by the cooling equipment. With steeply rising need for energy [4], it is predicted that the operation costs for power and cooling will soon exceed the acquisition cost [5].

The performance increase of microprocessors traditionally follows Moore's law [6] by shrinking the size of transistors so that an increasing number of transistors could be placed per unit area on a single chip. Over the last few years the increasing device density has also led to an increased power density because the transistor switching voltage could not be reduced fast enough. The resulting higher heat dissipation densities require new cooling solutions. Due to its superior thermal characteristics over the

* Corresponding author. Tel.: þ41 44 632 27 38; fax: þ41 44 632 11 76. E-mail address: dimos.poulikakos@ethz.ch (D. Poulikakos).

## ab s trac t

We report the energy and exergy efficiencies of Aquasar, the first hot water cooled supercomputer prototype. The prototype also has an air cooled part to help compare the coolants's performances. For example, a chip/coolant temperature differential of only 15  C was sufficient for chip cooling using water. The air cooled side, however, required air pre-cooling down to 23  C and a chip/coolant temperature differential of 35  C. Whereas extra exergy was expended for air pre-cooling, the higher thermal conductivity and specific heat capacity of water enabled coolant temperatures to be safely raised to 60  C. Using such hot water not only eliminated the need for chillers, it also opened up the possibility of heat reuse. The latter was realized by using the hot water from Aquasar for building heating. A heat recovery efficiency of 80% and an exergetic efficiency of 34% were achieved with a water temperature of 60  C. All these results establish hot water as a better coolant compared to air. A novel concept of economic value of heat was introduced to evaluate different reuse strategies such as space heating and refrigeration using adsorption chillers. It was shown that space heating offers the highest economic value for the heat recovered from data centers.

© 2012 Elsevier Ltd. All rights reserved.

traditional air cooling, single phase liquid cooling of electronic components is now a well-recognized and practically unavoidable alternative to address rising heat dissipation densities. The cooling demand in electronic chips is expected to rise continuously. For example, it is now clear that the power densities of the next generation 3D integrated chip designs will make switching to water cooling inevitable [7] and will also require specific attention to both hydrodynamic and thermal aspects simultaneously [8]. Starting from the work of Tuckerman and Pease [9], who established the concept of high-performance forced liquid cooling, several studies focused on the thermal performance of microchannel based heat sinks [10,11]. Recent studies have also exploited highly sophisticated interfaces for backside heat removal using direct liquid jet impingement in combination with manifold microchannel heat sinks [12,13]. The reduced thermal resistance of these interfaces decreases the temperature difference between the processors and the coolant, enabling coolant temperatures above the free cooling limit. Free cooling has no need for any active pre-cooling equipment rendering energy intensive chillers unnecessary. This reduces the energy and capital costs associated with running a data center and results in a more energy-efficient data center. Moreover, elevated coolant temperatures open up possibilities of energy reuse [14]. For example, the hot water from a data center can be used for building heating in moderate climates [15]. Such an energy reuse strategy can minimize the overall system carbon footprint [16].

Global actions to reduce carbon footprints are crucial because energy from fossil fuels accounts for over 70% of the world energy usage [17]. The reduction of the CO2 emissions achieved through energy reuse provides a viable path to reduce emissions in accordance with the international panel on climate change [18], the Stern report [19] and the effort is also aligned with the Kyoto protocol [20].

However, using only energy [21] as a measure to identify the benefits of such a system can be misleading because the quality of different kinds of energy is very different. Therefore, a system analysis has to be performed in terms of thermodynamic exergy [22], which specifies the quality of energy in addition to its available quantity [23]. Shah et al. [24] introduced an exergy based figure of merit for the evaluation of computational performance at chip level. Analyzing exergy destruction at the system level in air cooled data centers [25] provided crucial information about the usefulness of a green system. The minimization of exergy destruction in such a systemwill result in more environmentfriendly computing and will open new possibilities for the reuse of its significant waste heat.

In this paper, we report an experimental investigation, and the corresponding energy and exergy analyses based on Aquasar, the first hot water cooled supercomputer prototype. The prototype also has an air cooled part, which facilitated a direct comparison of water and air cooling options for data centers. The system allows a direct comparison of the new hot water cooling concept with traditional air cooling. The value of heat from Aquasar is determined for different reuse strategies. The work lays the foundation for developing environmental-friendly computing data centers with energy reuse and minimal carbon footprint.

## 2. TheAquasarsystem

Aquasar is a hot water cooled data center prototype with waste heat reuse. The system consists of 33 IBM BladeCenter QS22 PowerXCell and 9 IBM BladeCenter HS22 Intel Nehalem equally distributed in 3 IBM BladeCenter H Chassis with 14 BladeCenters in each chassis (see Fig. 1a). To compare the performances of liquid and air cooled electronic components, two of the three BladeCenter Chassis were retrofitted to enable liquid cooling while the third one was left air cooled. On the BladeCenter level, the copper and aluminum heat spreaders were replaced by a copper cooling loop as shown in Fig. 1 (b). Every component dissipating more than 3 Watts of power was directly connected to the cooling loop. Special attention was paid to the cooling of the processors. These were cooled by a manifold microchannel (MMC) heat sink specifically developed to address the cooling requirements of these processors. A more detailed description of the heat sink performance and design can be found elsewhere [26]. Additional temperature sensors were mounted on some BladeCenters to gather information about the temperature distribution and ensure reliable operation. The water as coolant was supplied via a manifold in the back plane of the chassis ensuring that each BladeCenter received the same amount of coolant. Fig. 2 shows the coolant supply network enabling heat transfer to the building heating grid. The coolant network consisted of three separate closed cycles. The different cycles were necessary to address the different purity requirements and to consistently prevent overheating of the system. The first cooling loop (referred as primary loop) consisted of the cooling structure in the BladeCenters, two filters (5 mm and 50 mm), sensors for measuring temperatures, pressure drops and the coolant flow rate, a heat exchanger and two gear pumps driving the flow while ensuring redundancy. The temperatures were measured using duct temperature sensors (TF 050 NI1000, sensortec GmbH, Switzerland) which were cross calibrated to make relative measurements with an accuracy of 0.1  C. Two differential pressure sensors (PDW-2,5U, sensortec GmbH, Switzerland) were used to measure the pressure drop over the filters and the BladeCenters with an accuracy of 0.5%. The coolant flow rate was measured using a turbine flow meter (Kobold, Germany) with an accuracy of 2.5%. The coolant in this loop was de-ionized water containing 0.1% of benzotriazole (BTA) as a corrosion inhibitor. The water purity requirements were stringent because of the copper MMC heat sink that is why two filters were used in the loop. The pressure drop across the filters and the BladeCenters was monitored to check for clogging that would result in an insufficient supply of coolant. The data gathered from the flow meter and the two temperature sensors, placed before and after the heat exchanger, were used to determine the heat rate passed from the primary loop to the intermediate loop.

<!-- image -->

Fig. 1. (a) Hot water cooled first of a kind data center: Aquasar. (b) Water cooled IBM BladeCenter QS22.

<!-- image -->

The intermediate loop, with no special requirements for the purity of the water, was introduced to supply the systemwith cold water in case of overheating in the primary loop. The intermediate loop received the heat through the primary heat exchanger (referred to as PHE in Fig. 2) and passed it through the second heat exchanger (referred to as SHE in Fig. 2) to the ETH heating grid. A three-way valve was installed before the secondary heat exchanger to vary the hot water flow across it. Controlling the hot water flow through the secondary heat exchanger helped to control the heat flow and to maintain a constant inlet temperature to the cold side of the primary heat exchanger. This arrangement helped to remove any temperature fluctuations on the building side from affecting the data center operation. A second three-way valve including drain was installed after the secondary heat exchanger to supply the systemwith cold water to prevent any accidental overheating of the system. To determine the heat flow, temperature sensors were placed before and after both heat exchangers and the liquid flow rate was measured using a flow meter. Moreover, the firmware of the electronic components gave direct access to the electric power consumption allowing the computation of the heat recovery efficiency. The power consumption, the reported temperatures from the BladeCenters as well as the flow, temperature, and pressure data from the primary cooling loop were stored in a mySQL database for subsequent analysis. The air cooled part of the system used chilled air with an inlet temperature of 23  C and a constant volumetric flow rate of 820 l/s. The exhaust air in the back passed a plate heat exchanger where 16  C water was used to cool down the air before it re-entered the BladeCenter Chassis again. The cold water was supplied by mechanical chillers operating with refrigerants at temperatures around 12  C. The mechanical chiller system subsequently lifted the temperature to 40  C using a vapor compression cycle to reject it to the ambient via a dry cooler.

The fact that air cooling was needed for the air cooled blades and the power supplies of the liquid cooled part of the Aquasar system resulted in additional challenges. If not properly controlled, the chilled air could leak to the hot water cooled portions and result in additional convective losses, thereby lowering the overall heat recovery efficiency. The air temperature could not be raised to minimize this effect because air is a much worse coolant than water. Water has an approximately 3500 times higher volumetric heat capacity and a 25 times higher thermal conductivity than air. The air cooled BladeCenters, the power supplies and the storage server imposed cooling constraints on the temperature and the amount of cold air that was circulating in the system. In addition, we must note that the entire electronic hardware was optimized for air cooling and the water cooling elements were retrofitted for the prototype demonstrator. First, this meant that the air had multiple entry points to the BladeServer to maximize the flow through the BladeServer. Secondly, there was an overpressure in the front due the fans of the chiller pre-cooling the air and there was a second aspirating fan in the rear responsible for a high airflow. To minimize air leaks, all air slots in the front and on the side of the two liquid cooled BladeCenter Chassis were closed using foam thermal insulation (HT Armaflex, Armacell Engineered Foams) and Kapton tape (Scotch 92, 3M). In addition, all the piping and the entire supplying structure of the liquid cooling loop were encased in Armaflex thermal insulation to reduce convection losses.

Fig. 2. Schematics of the cooling loop.

<!-- image -->

## 3. Characterization

## 3.1. Energyefficiency

The most relevant metric for secondary, heat reuse is the heat recovery efficiency and its variation with the coolant temperature. The heat recovery efficiency is the ratio of the rate of heat removal by the coolant and the consumed electrical power. The heat removal rate was calculated as

<!-- formula-not-decoded -->

\_

The Q was a function of the mass flow rate \_m, the specific heat c and the change in temperature.

The energy efficiency for data centers is assessed using standard metrics such as the power usage effectiveness (PUE) [27] and the energy reuse effectiveness (ERE) [21]. These metrics were introduced by the green grid [28], a reputable non-profit organization addressing power and cooling requirements of future data centers. The PUE value, defined as

<!-- formula-not-decoded -->

is a measure of how efficiently a data center is using power. The symbols PDataCenter, PCooling and PIT respectively denote the total power consumption of a data center, the power spent on cooling devices and the power spent on the IT equipment i.e. for computing, storage and network equipment. The lower the value of the PUE metric, the better the data center because a low PUE value implies that most of the energy consumed in a data center is actually used for computing. The PUE value does not take into account the possibility of heat reuse. Therefore, the metric ERE, defined as

<!-- formula-not-decoded -->

was used. ERE properly accounts for the new idea of benefits achieved by introducing waste heat reuse from a data center. The parameter Preuse denotes the power supplied to a secondary application, which is space heating for Aquasar.

## 3.2. Exergyanalysis

To evaluate the usefulness of the energy recovered from the data center, an exergy analysis needs to be performed. Exergy is a thermodynamic property, which helps assess the differences in the quality of different kinds of energy. Following standard thermodynamic practice, the electric power supplied to the data center is considered pure exergy whereas only a part of the heat recovered can be converted to useful work, which limits the exergy content of heat. The exergy content of the heat dissipated by the processors is given by

<!-- formula-not-decoded -->

Qel, Tel and T0 denote the amount of the dissipated heat, the surface temperature of the processors and the ambient reference temperature, respectively. The exergy gained by the coolant through the heat it recovers in course of flowing across the Aquasar system can be expressed as the difference in the flow exergies as

<!-- formula-not-decoded -->

The symbols h and s denote the enthalpy and the entropy of the coolant. Eq. (5) is also used to characterize the exergy gain of the intermediate coolant as it flows across the primary heat exchanger. The difference in the exergy gains of the primary and the intermediate coolants is essentially the exergy loss across the heat exchanger.

The exergy analysis of the air cooled part in the system needs to be performed separately because the temperature levels of the chilled air and the cold water (see Fig. 2) remain below the ambient temperature. Therefore, the evaluation of the change in the flow exergy would yield negative values for both inlet and outlet states of the air. In addition, the rise in temperature due to the heat transfer results in an outlet state closer to the ambient than the inlet state. To overcome the inconvenience of negative exergy, the exergy of such media can be evaluated using a reverse Carnot cycle. Under variable surface temperature, the resulting exergy transferred through a differential amount of heat transfer can be expressed as Ref. [29].

<!-- formula-not-decoded -->

The differential exergy in Eq. (6) can be integrated to produce an expression for the exergy gain as function of the initial and the final temperatures

<!-- formula-not-decoded -->

The exergy analysis is completed by a calculation of the 2nd law efficiency for the primary and the intermediate liquid cooling cycle (see Fig. 2) given as

<!-- formula-not-decoded -->

The symbols Exel and Ppump denote the electric input and the pumping power needed to drive the coolant through the cooling structure.

## 3.3. Application specific economic value of recovered heat

Typically, heat is not considered a valuable energy form due to its low exergetic content. However, the economic value of heat can be significantly different because the otherwise wasted heat can be used in secondary applications, which conventionally use combustion of fossil fuels to obtain the required heat. Therefore, we introduce a new metric called economic value of heat (VH) in order to quantify the benefits of heat recovered from hot water cooled data centers as

<!-- formula-not-decoded -->

## Cost of 1 kWh heat from data centers

The cost of heat recovered from data centers is, in turn, related to the cost for electricity consumed by the data centers and the heat recovery efficiency as

Cost of 1 kWh heat from data centers

<!-- formula-not-decoded -->

The application specific economic value of the recovered heat was determined using country specific information on cost for electricity and fossil fuels for reuse strategies such as space heating, refrigeration based on adsorption chillers and desalination. However, a thermal energy reuse strategy requires the definition of a certain minimal temperature threshold, in order for the hot water coming from the data center to be energetically useful. The higher the water temperature above this threshold, the easier it is to utilize heat through multiple means. For example, space heating based on standard wall radiators needs a higher temperature than that based on floor-installed heat exchangers. Therefore, at a sufficiently high temperature, both these applications are feasible avenues for heat reuse, thereby improving the utility of heat. Clearly, a parameter is needed to account for this temperature-specific variation in the utility of heat for any given reuse application and the economic value of heat introduced above should be modified to reflect this temperature dependence. We account for this important aspect by introducing an application specific utility function (U) in the above definition of the economic value of heat. For every reuse application, the value of the utility function should vary from zero to one over a specific range of temperature and thereafter remain constant. Clearly, such a utility function is system-specific and will also depend on the preferences of the designer. To illustrate the underlying concept, in the current work we used sigmoid functions to obtain the application specific utility functions. The employed utility functions are plotted in Fig. 3. The temperature range over which the utility function went from zero to one was 40  Ce70  C for space heating, 65  Ce90  C for refrigeration, and 55  Ce80  C for desalination. With inclusion of the utility function, the economic value of heat can be redefined as

<!-- formula-not-decoded -->

## 3.4. Uncertaintyanalysis

The uncertainties in the physical measurements of temperature, pressure, flow and consumed power were mentioned above in the system description. These parameters were measured separately and therefore considered to be independent of each other. The experimental uncertainty of the measured heat rate was calculated using propagation of error [30] as follows:

<!-- formula-not-decoded -->

The uncertainties for the exergy values were also calculated in a similar manner.

## 4. Results

## 4.1. Energy

The parameters of a data center relevant for secondary, heat reuse applications were analyzed first. Fig. 4 and Fig. 5 show the results. To this end, the two most important parameters are the heat recovery efficiency and the temperature level at which the heat is available. The recovered heat was evaluated as a function of the coolant inlet temperature under three different working conditions which cover the entire working range of the system (i.e. the data center). The condition labeled 'Full load,' describes the system operating at full computational capacity. This is achieved by running a full load exerciser. The second working condition labeled 'Idle' describes the system powered on and operating without any additional computational load. These two working conditions represent the boundaries of the normal working condition of a real data center. The last working state labeled 'Power off' describes the systemwith no electrical power applied to the servers. This mode was tested to determine a lower reference for the power (heat) loss to the ambient since the system runs at a temperature well above the ambient. Fig. 4 (a) displays the electric power delivered to (and consumed by) the system and the heat recovered from it as a function of the water inlet temperature. The power consumption of the electronic components increases by 7  1% as the coolant temperature rises from 30  C to 60  C. This effect is due to the increase in the electric resistances in the communication wires and the leakage currents in the microprocessors. Fig. 4 (a) also shows a simultaneous decrease in the amount of heat recovered because with an increase in water inlet temperature the system operates at an overall higher temperature. The resulting higher temperature difference to the ambient leads to increasing losses due to natural convection. All the careful measures to minimize air leaking to the liquid cooled components resulted in a heat recovery efficiency of 80% for the 'Full load' operating system at an inlet temperature of 60  C. Fig. 4 (b) shows the recovery efficiencies for the working modes 'Full load' and 'Idle'. As expected the recovery efficiency decreases as a function of temperature, however, the decrease of the recovery efficiency for the idle working mode is significantly steeper. This indicates that the higher the computational load, the better the thermal performance of the system. Fig. 5 shows the variation of lost power with water inlet temperature. Within the measurement error, clearly the different load conditions coincide and the power loss from the system appears only to be a function of the coolant temperature. The similarity of the measured absolute power losses for all working modes implies that the heat generated on BladeServer level is very well captured by the coolant. Thus the cooling structure is very efficient in capturing the heat of all attached electronic components and the losses to the ambient are not affected by the applied computational load in the system. The losses to the ambient are dictated by the conduction of heat from the BladeServers to the chassis, the losses in the pumping module and the losses in the piping necessary to transfer the heat to the heating grid. This shows the need for an effective insulation for such thermal energy recovery systems.

Fig. 3. Utility functions for different reuse strategies.

<!-- image -->

Fig. 4. Energy budget in the water cooled data center. (a) Power consumed and recovered and (b) Recovery efficiency as a function of the coolant temperature.

<!-- image -->

<!-- image -->

The next step was the evaluation of the general performance of data centers using the PUE and ERE values. The PUE value as a function of the coolant temperature can be seen in Fig. 6. The PUE for Aquasar stays constant at a value of 1.15, within the experimental error, for the entire working range. For comparison, an industry average air cooled data center has a PUE around 2.5 [5]. The value of PData Center is difficult to determine [31] because the energy spent on support, security and emergency must also be included and is not known accurately a priori. This sometimes results in implausible PUE claims. The lowest claimed PUE values are all based on the principle of free cooling discussed in the introduction section. The reduction in PUE for Aquasar compared to a traditional data center is due to the reduced energy spent for the cooling loop. The ERE values were also plotted in Fig. 6 as a function of the coolant temperature. The ERE value increased for elevated coolant temperatures because of the decreasing recovery efficiency. This value is highly dependent on the effectiveness of the data center insulation and the temperature difference between the system and its immediate surroundings.

## 4.2. Exergyanalysis

An exergy analysis was performed to identify the major sources for exergy destruction in Aquasar. T0 ¼ 30  C was chosen as ambient temperature because it corresponded to the laboratory temperature which was not actively regulated. Fig. 7 depicts the control volumes used to evaluate the relevant exergy contents in different parts of the data center. In all instances shown we include both the coolant and the server in our control volume definitions. The exergy at chip level is the first quantity of interest and it is evaluated by analyzing the control volumes marked by green rectangles in Fig. 7 (a). The control volumes consist of electronic components such as the microprocessors because their temperature determines the quality of the dissipated heat. The exergy gain of the primary coolant on the hot side of the primary heat exchanger is the second quantity of interest. The flow exergy gain is computed as the difference in flow exergy between inlet and outlet ports to the components within the control volume marked by green rectangles in Fig. 7 (b). The exergy computed in this way is a measure of the exergy available from the electronic components after taking in to account the irreversibilities associates with the pumping losses for coolant circulation, heat loss from the main system and heat transfer across a finite temperature differential. Eq. (5) is also used to characterize the exergy gain of the second coolant, i.e. at the cold side of the primary heat exchanger, to determine the exergy loss across the heat exchanger. The results for the three different positions are plotted in Fig. 8a for the data center operating at full load. This becomes even clearer if we notice that the electric power consumption plotted in Fig. 4 (a) is nearly 7 kW or higher, whereas maximum exergy gains (recovered) plotted in Fig. 8 (a) remain under 1000 W. Clearly, the highest loss of exergy is due to the conversion of electricity to heat during the operating time of the electronic components. This can be better understood by considering two numerical examples. According to Eq. (4), using water at 30  C as coolant e with a resulting chip temperature of 45  C e and assuming an ambient temperature of 30  C, this conversion accounts for a loss of 95% of the initial available exergy. The loss can be reduced to 87% by switching to hot water at a temperature of 60  C as coolant and thereby raising the operating temperatures of the processors to an average of 75  C. A similar tendency is seen for the exergy gain of the primary coolant shown in Fig. 8 (a). The available exergy at the heat exchanger is increased although the energy passing through the heat exchanger is decreased due to higher thermal losses to the ambient at elevated temperatures. The main reason for the exergy destruction between the chip and the primary coolant is the heat transfer across a finite temperature difference. Reducing this difference results in a lower exergy destruction. The last exergy change of interest is the exergy gain of the intermediate coolant as it flows through the primary heat exchanger. The control volumes (green rectangles) in Fig. 7 (c) can be used to evaluate this exergy gain. The result is plotted in Fig. 8 (a) and it shows that the exergy destruction across the heat exchanger is negligible compared to the exergy loss due the conversion from electricity to heat. However, this is a source of exergy destruction that can be reduced through a better design of the exchangers. The smaller the temperature difference between the coolant in the primary and in the intermediate loop, the smaller the exergy destruction across this heat exchanger.

Fig. 5. Absolute power loss as a function of the coolant temperature.

<!-- image -->

Fig. 6. Data center metrics describing energy efficiency with (ERE) and without (PUE) energy reuse.

Fig.7. Importantlocationsfortheexergyanalysis.(a)Heatgeneratedbytheelectronic components during operation (b) Primary cooling cycle (c) Intermediate cooling cycle. The control volumes analyzed are marked within green rectangles. (For interpretation of the references to colour in this figure legend, the reader is referred to the web version of this article.)

<!-- image -->

Fig. 8. (a) Exergy at different positions in the water cooled part of the Aquasar system. (b) Direct comparison of the available exergy for air and water cooling.

<!-- image -->

The exergetic output from the air and the liquid cooling approaches need to be critically analyzed in order to underscore the benefits of hot water cooling. Within measurement error, the coolant flow rates (on both water and air cooled sides) were kept constant in this study. As a result, for the different coolant temperatures tested, the temperature difference between chip and coolant was over 35  C for air cooling and 15  C for water cooling. The detailed temperature measurements are not shown for brevity. In order to obtain a fair comparison, the exergy gains in the air and liquid cooled cases should be compared at the same chip temperature. Therefore, in Fig. 8 (b) the exergy gains at 23  C for the air cooled case should be compared with that of 45  C for the liquid cooled case. Clearly, with water we have a much higher gain in exergy due to lower temperature difference between the chip and the coolant. In this context, it is important to mention that with air cooling an additional exergy penalty is always present due to the use of chillers which are needed to reduce the air temperature. In addition, no reuse of the waste heat is possible because of the low coolant outlet temperature.

The second law efficiencies computed from measured temperatures, flow rates and pressure drops are plotted in Fig. 9 as a function of the coolant inlet temperatures. The most dominant term in Eq. (8) is the electricity which is considered as pure exergy. The rise in the second law efficiency with the increase in the coolant inlet temperature is due to \_ Exout being highly temperature dependent. Therefore, it is essential to increase the coolant temperature and to minimize the decrease in temperature between the liquid cooled electronic parts of the data center and the heat reuse application. The influence of the introduction of an intermediate loop to prevent overheating in the Aquasar system results in the different exergetic efficiencies from the primary and the intermediate cooling cycles. The decrease in temperature between the primary and the intermediate cooling cycles accounts for a reduction of the exergetic efficiency of up to 40%. The highest measured efficiency was 34% for the internal loop at the highest coolant inlet temperature.

Fig. 9. Second law efficiencies of the primary and intermediate liquid cooling cycle.

<!-- image -->

Fig. 10. Value of heat for different applications.

<!-- image -->

## 4.3. Application specific economic value of recovered heat

The economic value of heat is very distinct for the different secondary reuse applications. In addition, costs for electricity and fossil fuels are country specific [32] making the location of the data center an important decision. Fig. 10 shows the results for Switzerland (CH) [33,34] as an illustrative example. The recovery efficiency (h1st) was taken from the measurements plotted in Fig. 4 (b). The value of heat increases as a function of the temperature. However, this effect competes against the decreasing recovery efficiency which is dominant at higher temperatures. As a result the optimal working range of a data center may not be at the highest possible temperature. One can consider the Carnot efficiency factor,  1 T0=Tel  , from Eq. (4) as the normalized exergetic content per unit heat output. This temperature dependent exergetic content of the heat was added to Fig. 10 in order to show that the economic value of heat can be higher than its exergetic content. The reason for this is the possibility of a direct use of the heat without the need of a conversion back to mechanical work. The value of heat for refrigeration based on adsorption chiller was assessed using mechanical chillers as a reference. The low coefficient of performance for current commercial adsorption chillers is responsible for the low value of heat in the refrigeration reuse strategy in countries like Switzerland. However, this is in contrast with countries such as Saudi Arabia (SA) where for domestic consumers the price for 1 kWh electricity rises with increase in their consumption [35]. Such a scenario could significantly increase the value of heat for refrigeration.

In order to put things in context, one must also analyze the potential benefits of direct electricity generation using the heat extracted from the data centers. Therefore, the possible electricity generation based on a Rankine cycle [36] (with 50% efficiency) was added to show that such a strategy is not economically favorable relative to other secondary usage alternatives. Overall, by comparing the different VH trends in Fig. 10 we can see that for coolant temperatures in the working range of the Aquasar system (30  Ce65  C), space heating is the most promising reuse strategy. Other reuse strategies could only become economically interesting if the coolant temperatures could be increased by smaller (&lt;5  C) gradients between electrical components and coolant or when coolant temperatures can be lifted by combining solar thermal systems with data centers in hot and sunny climates.

## 5. Conclusions

Using measurements and analyses on a data center prototype called Aquasar, we have demonstrated that the cooling requirements in data centers can be efficiently addressed by using hot water as coolant. The lower thermal resistance of liquid cooled heat sinks enabled the coolant temperature to be raised to 60  C. With chilled air at 23  C the processors in the air cooled side of the data center could be cooled with a temperature differential of 35  C. Clearly, considerable exergy is also expended to pre-cool the air. On the other hand, the hot water at 60  C could be effectively used to cool the processors on the water cooled side with a temperature differential of only 15  C. The benefits of the liquid cooled solution were the higher exergetic output and the possibility of a direct use of up to 80% of the recovered heat for space heating. The energy efficiency metrics PUE and ERE of this hot water cooled data center were significantly better than in industry averaged air cooled data centers because no additional coolant chillers were required which normally use as much energy as all the electronic components together. Switching to hot water as coolant increases the exergetic efficiency up to 34% for the highest operation temperatures. Reuse strategies such as space heating and refrigeration using adsorption chillers were tested as potential means to use waste heat from data centers. It was shown that an application specific analysis of the economic value of the recovered heat can provide additional information about the best reuse strategy. Direct use of data center heat for space heating provided the highest economic value of heat for the system under investigation.

## References

- [1] Koomey JG. Worldwide electricity used in data centers. Environmental Research Letters 2008;3(3).
- [2] Meijer GI. Cooling energy-hungry data centers. Science 2010;328:318e9.
- [3] Mitchell-Jackson J, Koomey JG, Nordman B, Blazek A. Data center power requirements: measurements from Silicon Valley. Energy 2003;28(8):837e50.
- [4] Rattner AS, Garimella S. Energy harvesting, reuse and upgrade to reduce primary energy usage in the USA. Energy 2011;36(10):6172e83.
- [5] Scaramella J. Worldwide server energy expense 2009e2013 forecast. International Data Corperation; 2009.
- [6] Moore GE. Cramming more components onto integrated circuits. Electronics; 1965:114e7.
- [7] Alfieri F, Tiwari MK, Zinovik I, Poulikakos D, Brunschwiler T, Michel B. 3D integrated water cooling of a composite multilayer stack of chips. Journal of Heat Transfer-Transactions of the Asme 2010;132(12):121402.
- [8] Renfer A, Tiwari MK, Brunschwiler T, Michel B, Poulikakos D. Experimental investigation into vortex structure and pressure drop across microcavities in 3D integrated electronics. Experiments in Fluids 2011;51(3):731e41.
- [9] Tuckerman DB, Pease RFW. High-performance heat sinking for VLSI. Electron Device Letters 1981;2(5):126e9.
- [10] Colgan EG, Furman B, Gaynes M, GrahamWS, LaBianca NC, Magerlein JH, et al. A practical implementation of silicon microchannel coolers for high power chips. IEEE Transactions on Components Packaging Technology 2007;30(2):218e25.
- [11] Lee PS, Garimella SV, Liu D. Investigation of heat transfer in rectangular microchannels. International Journal of Heat and Mass Transfer 2005;48(9): 1688e704.
- [12] Brunschwiler T, Rothuizen H, Fabbri M, Kloter U, Michel B, Bezama RJ, et al. Direct liquid jet-impingement cooling with micron-sized nozzle array and
13. distributed return architecture. In: Conference Direct Liquid Jet-Impingement Cooling with Micron-Sized Nozzle Array and Distributed Return Architecture, vol. 1 and 2; 2006. 196e203.
- [13] Escher W, Michel B, Poulikakos D. A novel high performance, ultra thin heat sink for electronics. International Journal of Heat and Fluid Flow 2010;31(4): 586e98.
- [14] Stijepovic MZ, Linke P. Optimal waste heat recovery and reuse in industrial zones. Energy 2011;36(7):4019e31.
- [15] Brunschwiler T, Meijer GI, Paredes S, Escher W, Michel B. Direct waste heat utilization from liquid-cooled supercomputers. Conference Direct Waste Heat Utilization From Liquid-Cooled Supercomputers, Washington; 2010. p. 23352.
- [16] Brunschwiler T, Smith B, Ruetsche E, Michel B. Toward zero-emission data centers through direct reuse of thermal energy. IBM Journal of Reseasrch and Development 2009;(3):53. Paper 11.
- [17] Key World Energy Statistics. International Energy Agency; 2010.
- [18] Climate Change 2007dmitigation of climate change. Intergovernmental Panel on Climate Change 2007.
- [19] SternN.Sternreviewontheeconomicsofclimatechange,www.hm-treasury. gov.uk/sternreview\_index.htm; 2007 [accessed 10.04.12].
- [20] Kyoto Protocol. United Nations Framework Convention on climate Change1997.
- [21] Patterson M, Tschudi B, Vangeet O, Cooley J, Azevedo D. A metric for measuring the benefit of reuse energy from a data center. The Green Grid; 2010.
- [22] Groscurth HM, Kummel R, Vangool W. Thermodynamic limits to energy optimization. Energy 1989;14(5):241e58.
- [23] Moran MJ, Shapiro HN. Fundamentals of engineering thermodynamics. 6th ed. Hoboken, USA: John Wiley &amp; Sons; 2008.
- [24] Shah AJ, Carey VP, Bash CE, Patel CD. An exergy-based figure-of-merit for electronic packages. Journal of Electronic Packaging 2006;128(4):360e9.
- [25] Shah AJ, Carey VP, Bash CE, Patel CD. Exergy analysis of data center thermal management systems. Journal of Heat TransfereTransactions of the Asme 2008;130(2):021401.
- [26] Kasten P, Zimmermann S, Tiwari MK, Michel B, Poulikakos D. Hot water cooled heat sinks for efficient data center cooling: towards electronic cooling with high exergetic utility. Frontiers in Heat and Mass Transfer 2010;1(2). 023006.
- [27] Haas J, Froedge J, Pflueger J, Azevedo D. Usage and public reporting guidelines for the green grid's infrastructure metrics PUE/DCiE the green grid; 2009.
- [28] Thegreengrid.www.thegreengrid.org/. [accessed10.04.12].
- [29] Balta MT, Kalinci Y, Hepbasli A. Evaluating a low exergy heating system from the power plant through the heat pump to the building envelope. Energy and Building 2008;40(10):1799e804.
- [30] Taylor JR. An introduction to error analysis: the study of uncertainties in physical measurements. 2nd ed. New Jersey, USA: University Science Books; 1997.
- [31] Neudorfer J. Top 10 things data centers forget about PUE. CTOEDGE, www. ctoedge.com/content/top-10-things-data-centers-forget-about-pue; 2011 [accessed 10.04.12].
- [32] Europe's energy portal. www.energy.eu. [accessed 10.04.2012].
- [33] EKZ. Industrial tariffs untill 100'000 kWh (In German). www.ekz.ch/content/ ekz/de/geschaeftskunden/stromprodukte/kunden-ab-1-gwh/ekz-mixstrom. html#tab2. [accessed 10.04.12].
- [34] Erdöl-Vereinigung. Monthly averaged pricing for domestic fuel oil (In German). www.erdoel-vereinigung.ch/de/heizenmitoel/Peise/HeizoelpreiseMonatsmittel. aspx. [accessed10.04.2012].
- [35] Saudi Electricity Company. Kingdom of Saudi Arabia electricity tariffs. www. dynamic-ews.com/Tariffs/Electricity%20Tariffs/KSA.pdf. [accessed 10.04.12].
- [36] Hung TC, Shai TY, Wang SK. A review of organic Rankine cycles (ORCs) for the recovery of low-grade waste heat. Energy 1997;22(7):661e7.