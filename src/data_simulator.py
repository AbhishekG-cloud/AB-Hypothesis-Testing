import numpy as np


class DataSimulation:
    def __init__(self):
        pass
    
    def simulate_A_B(self,n_visitors_A:int,n_visitors_B:int,A_prob:float,B_prob:float,size:int,seed:int):
        """
        Simulates an A/B test using a Binomial distribution.

        Args:
            n_visitors_A:
                Number of visitors assigned to variant A.

            n_visitors_B:
                Number of visitors assigned to variant B.

            A_prob:
                True conversion probability for variant A.

            B_prob:
                True conversion probability for variant B.

            size:
                Number of independent experiments.

            seed:
                Random seed for reproducibility.

        Returns:
            Dictionary containing observed conversion
            rates and uplift.
        """
        rng = np.random.default_rng(seed)

        
        A_conversions = rng.binomial(n_visitors_A,A_prob,size=size)
        B_conversions = rng.binomial(n_visitors_B,B_prob,size=size) 

        A_conversions = np.mean((A_conversions))
        B_conversions = np.mean((B_conversions)) 

        A_rate = (A_conversions/n_visitors_A)*100
        B_rate = (B_conversions/n_visitors_B)*100
        uplift = ((B_rate-A_rate)/A_rate)*100
        ## table summary
        print(f"""
            Visitors_A = {n_visitors_A}
            Visitors_B = {n_visitors_B}
            ------------------------------
            Conversion A   = {A_conversions}
            Conversion B = {B_conversions}
            -------------------------------
            Rate A = {A_rate:.2f}%
            Rate B = {B_rate:.2f}% 
            -------------------------------
            Uplift = {uplift:.2f}%



            """)
        return {
        "A_rate": A_rate,
        "B_rate": B_rate,
        "uplift": uplift
        }
        
scene_1 = DataSimulation()
first_case = scene_1.simulate_A_B(n_visitors_A=1000,n_visitors_B=1000,A_prob=0.1,B_prob=.1,size=5,seed=18)
second_case = scene_1.simulate_A_B(n_visitors_A=1000,n_visitors_B=1000,A_prob=0.1,B_prob=.12,size=5,seed=18)
third_case = scene_1.simulate_A_B(n_visitors_A=1000,n_visitors_B=1000,A_prob=0.1,B_prob=.2,size=5,seed=18)

print(first_case,"\n",second_case,"\n",third_case)