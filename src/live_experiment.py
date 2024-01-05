#!/usr/bin/env python3

""" 
@Author: Zeyu Pang, Daniel Tozadore
@Date: 05.01.2024
@Description : Live experiment Class
	Facilitate interaction with users during experiments, and save critical data in the live-stream mode
"""


from typing import Any
import rospy
from std_msgs.msg import String,Bool
import os
import csv
import sys


# Config colors of printing 
GREEN = "\033[0;32m"
BLUE="\033[0;94m"
RESET="\033[0m"


class Live_experiment:
    def __init__(self):
        
        # Basic preparation
        self.fps = rospy.get_param("/image/fps", "30")
        self.init=True
        self.round=0
        self.username=''
        self.folder_path='/home/student/catkin_ws_PANG/src/Live_Experiment/data'      # to be re-defined after moving !!!

        # Initial conditions
        self.state = ""
        rospy.Subscriber("/state_manager/state", String, self.setState)
        self.Idle_init=True
        self.Record_init=True
        self.Inference_init=True
        self.LLM_init=True
        self.LLM_done=False
        rospy.Subscriber("/video_builder/LLM_done", Bool, self.is_LLM_done)

        # Get 4 time points
        self.AVSR_start_time=0
        self.AVSR_end_time=0
        self.LLM_first_time=0
        self.LLM_last_time=0
        rospy.Subscriber("/video_builder/AVSR_start", String, self.get_AVSR_start_time)
        rospy.Subscriber("/video_builder/AVSR_end", String, self.get_AVSR_end_time)
        rospy.Subscriber("/video_builder/LLM_first", String, self.get_LLM_first_time)    
        rospy.Subscriber("/video_builder/LLM_last", String, self.get_LLM_last_time)   

        # Get 2 results
        self.AVSR_result=''
        self.LLM_result=''
        rospy.Subscriber("/video_builder/result", String, self.get_AVSR_result)
        rospy.Subscriber("/video_builder/LLM", String, self.get_LLM_result)
        rospy.Subscriber("/video_builder/LLM_words", String, self.print_LLM_words)

        # Publisher to state_manager
        self.pub_record_done = rospy.Publisher("/video_builder/record_done", Bool, queue_size=1)


    # Other tool functions    
    def setState(self, msg):
        self.state = msg.data
    
    def is_LLM_done(self,msg):
        self.LLM_done=msg.data
    
    def get_AVSR_start_time(self,msg):
        self.AVSR_start_time=float(msg.data)

    def get_AVSR_end_time(self,msg):
        self.AVSR_end_time=float(msg.data)

    def get_LLM_first_time(self,msg):
        self.LLM_first_time=float(msg.data)
    
    def get_LLM_last_time(self,msg):
        self.LLM_last_time=float(msg.data)

    def get_AVSR_result(self,msg):
        self.AVSR_result=msg.data
        sys.stdout.write(BLUE)
        print('{}:'.format(self.username),end=' ')
        print(msg.data)
        sys.stdout.write(RESET)
    
    def get_LLM_result(self,msg):
        self.LLM_result=msg.data

    def print_LLM_words(self,msg):
        sys.stdout.write(GREEN)
        print(msg.data, end=" ", flush=True)
        sys.stdout.write(RESET)


    # The main call function
    def __call__(self):
        rate = rospy.Rate(self.fps)

        while not rospy.is_shutdown():

            # Initialise experiment 
            if self.init==True:
                print('\n')
                print('Hello, dear my friend! Welcome to our experiment!')
                self.username=input('Please enter your name (could use a nickname if you want):')
                print('Hi! Dear {}~'.format(self.username))
                self.init=False

            # Interaction during different states
            if self.state == "Idle":
                if self.Idle_init==True:
                    if self.round==0:
                        print("\r")
                        print('This is Round 0 for test, please click on the camera-live-window, and then press SPACE to start chatting with me!')
                    elif self.round==1:
                        print('\n')
                        print('Now the experiment officially starts, we will do 5 rounds conversation~')
                        print('press SPACE to start Round 1 !!!')
                    else:
                        print('\n')
                        print('I am ready for another Round, press SPACE to start again!')
                    self.Idle_init=False  
            
            elif self.state == "Recording":
                if self.Record_init==True:
                    print('\r')
                    print('Round {} starts!'.format(self.round))
                    print('I am listening...')
                    self.Record_init=False

            elif self.state == "Inference":
                if self.Inference_init== True:
                    print('I am understanding...')
                    print('\r')
                    self.Inference_init=False
            
            elif self.state == "LLM":
                if self.LLM_init==True:
                    print('\r')
                    print('I am thinking...')
                    print('\r')
                    self.LLM_init=False
                
                if self.LLM_done==True:

                    if self.round!=0:
                        # Save the experiment data in a .csv file

                        ## difine the file path
                        file_name=self.username+'.csv'
                        file_path=os.path.join(self.folder_path,file_name)

                        ## calculate 3 needed time
                        AVSR_time=round(self.AVSR_end_time-self.AVSR_start_time,3)
                        thinking_time=round(self.LLM_first_time-self.AVSR_end_time,3)
                        talking_time=round(self.LLM_last_time-self.LLM_first_time,3)

                        ## create the data of current round
                        contents=[self.round, AVSR_time, thinking_time, talking_time, self.AVSR_result, self.LLM_result]
                    
                        ## write file
                        with open(file_path,'a') as file:
                            csv_writer=csv.writer(file)
                        
                            ### write head labels
                            if self.round==1:
                                labels=['Round','AVSR_time','Thinking_time','Talking_time','AVSR_result','LLM_response']
                                csv_writer.writerow(labels)
                        
                            ### write data of current round
                            csv_writer.writerow(contents)
                    

                    # End the experiment after 10 rounds
                    if self.round==5:
                        print('\n')
                        print('Experiment is over!')
                        print('Thank you so much for your cooperation and patience! Have a nice day~')
                        print("Merry Christmas in advance~")
                        rospy.signal_shutdown('Experiment finished.')


                    # Update initial conidtions
                    self.Idle_init=True
                    self.Record_init=True
                    self.Inference_init=True
                    self.LLM_init=True
                    self.LLM_done=False
                    self.round+=1

                    # Update state to state_manager
                    self.pub_record_done.publish(True)
                    
                    

            rate.sleep()



# The main running
if __name__=='__main__':

    rospy.init_node('live_experiment')
    live_experiment=Live_experiment()       # __init__

    try:
        live_experiment()                   # __call__
    except rospy.ROSInterruptException:
        pass


