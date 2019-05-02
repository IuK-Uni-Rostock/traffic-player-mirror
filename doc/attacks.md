# Attacks

Once everything is set up, attacks can be started when visiting the website of the control server which is http://127.0.0.1:8080/ by default. Usually, an attack consists of many different parameters which are required to create flexible attacks. All attacks have sane default values for the parameters. Some of these parameters are shared between attacks, for example the target players and a seed. To achieve reproducibility of attacks a seed is used for the pseudorandom number generator (PRNG), which when initialized with the same seed will always produce the same sequence of random numbers. The target players are used to specify which traffic players will execute the attacks on the fieldbus. If more than one traffic player is chosen, the telegrams are split up equally to all selected traffic players.

Below follows an explanation of the specific parameters for each currently implemented attack.

## Replay

The replay-attack does replay previously captured telegrams from the fieldbus. The captured telegrams are stored in chronological order in a local database. Besides the shared parameters, the parameters for the replay-attack are explained below. The order is always preserved, regardless of parameter choice.

| Parameter    | Type     | Example                    | Description  |
|---           |---       |---                         |---           |
| Replay speed | Float | 1 | The replay speed is used to modify the time between each telegram. A higher value, e.g. 2, will double the time between telegrams, thus slowing the attack down. A value of 0.5 will halve the time between telegrams, thus speeding the attack up. A value of 1 preserves the original time between telegrams. |
| Start time | Datetime | 2018-11-20 09:00:00.000000 | Starting at the start time, the telegrams will be used from the database for the replay attack. |
| End time | Datetime | 2018-11-20 09:15:00.000000 | The end time specifies the end of the time span. All telegrams between `start_time <= t <= end_time` are considered. |
| Selection rate | Integer | 50 | The selection rate specifies what percentage of the considered telegrams are selected for the replay attack. The PRNG is used to randomly select the telegrams. A value of 50 will select 50% of the telegrams. Allowed are values between 1 and 100. |

## Denial of Service (DoS)

The DoS-attack is used to disturb the continuous flow of telegrams by sending an enormous amount of randomly generated telegrams on the fieldbus. The generation of the telegrams is controlled by the following parameters.

| Parameter    | Type     | Example                    | Description  |
|---           |---       |---                         |---           |
| Workload     | Integer  | 100 | The workload describes how much capacity of the fieldbus should be used by the DoS-attack. A value of 100 means 100% capacity. Allowed are values between 1 and 100. |
| Duration     | Integer  | 300 | The duration specifies the length of the attack. The capacity of the fieldbus will be at the desired workload for the whole duration. |
| Telegram types | List of strings | ['A_GroupValue_Write'] | For the DoS-Attack only telegrams with the chosen telegram types are generated. |
| Target | String | 'LED Strips' | The target specifies which target addresses are used for the generated telegrams. Currently implemented targets are `LED Strips` and `Random`. |

## Walking Persons

The so called walking persons attack simulates persons walking inside a building, which can be used for testing of physical intrusion detection systems. Predefined scenarios are used for the buildings and paths of the persons. The produced traces by the motion sensors are merged with real telegrams from same database as used by the replay attack. The order of the telegram timestamps is preserved. Afterwards the merged sequence of telegrams is send to the fieldbus.

| Parameter    | Type     | Example                    | Description  |
|---           |---       |---                         |---           |
| Walking speed | Float | 2 | Describes the walking speed of the persons. A value of 2 means 2 m/s. Allowed are values between 0.1 and 10. |
| Jitter | Float | 0.5 | The jitter describes the variance of the walking speed. A value of 0.5 means that the walking speed does vary between -0.5 m/s and 0.5 m/s. Allowed are values between 0 and 10. |
| Start time | Datetime | 2018-11-20 09:00:00.000000 | Starting at the start time, the telegrams will be used from the database to merge with the generated motion sensor trace. |
| End time | Datetime | 2018-11-20 09:15:00.000000 | The end time specifies the end of the time span. All telegrams between `start_time <= t <= end_time` are considered. |
| Scenario | Integer | 1 | Describes which predefined scenario to execute with the given parameters. Currently implemented scenarios are: Scenario 1, which is scenario for testing and debugging; Scenario 2, which represents the 3rd floor of the KZH and two persons walking to their opposite sides. |