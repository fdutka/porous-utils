import pandas as pd
import argparse

def experiment_end(tstart, flowrate, volume = 110):
    duration = volume/flowrate
    tend = pd.to_datetime(tstart)+pd.Timedelta(f"{duration}H")
    print(f"End of experiment on: \n {tend.day_name()}, {tend}")

__all__ = ['experiment_end']    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Script printing end time of experiment 
        
        Example:
        python experiment_end_date.py 2018-08-03_19:00:00 0.5 110
        
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('tstart', help='timestart of experiment start')
    parser.add_argument('flowrate', help='absolute flowrate in ml/h')
    parser.add_argument('volume', help='absolute volume of syringes in ml')
    args = parser.parse_args()
    
    tstart = " ".join(args.tstart.split("_"))
    
    experiment_end(tstart, float(args.flowrate), float(args.volume))
    
    

