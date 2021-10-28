#!/usr/bin/env python3

class TestBase:
    def __init__(self):
        self.profiles = list()

    def pre_clean_up(self):
        if self.profiles:
            for profile in self.profiles:
                profile.precleanup()

    def clean_up(self):
        if self.profiles:
            for profile in self.profiles:
                profile.cleanup()

    def start(self):
        if self.profiles:
            for profile in self.profiles:
                profile.start()

    def stop(self):
        if self.profiles:
            for profile in self.profiles:
                profile.stop()

    def build(self):
        # - create station profile
        # - create 2 criteria [ex: not down, continually_receiving] object (for ex)
            # - station_profile.add_criteria([not_down, continually_receiving, etc_3])
            # design - inversion of control 

        if self.profiles:
            for profile in self.profiles:
                profile.build()

    def passes(self):
        if self.profiles:
            for profile in self.profiles:
                profile.check_passes()
        
    def run_duration(self, monitor_enabled= False):
        #here check if monitor is enabled or not, then run loop accordingly
        self.check_for_halt()
        if self.profiles:
            if monitor_enabled:
                for profile in self.profiles:
                    profile.monitor_record() #check for halt in monitor record? 
            for profile in self.profiles:
                profile.grade()
        if self.exit_on_fail:
            if self.fails():
                self.exit_fail()
        self.check_for_quit()
         
    def report(self, enabled= False):
        #here check if monitor is enabled or not, then run loop accordingly with lfreporting
        pass

    def begin(self):
        self.pre_clean_up()
        self.build()
        self.start()    
        self.run_duration()
        self.stop() 
        self.report()
        self.clean_up()  

