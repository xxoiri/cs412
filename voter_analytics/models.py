# voter_analytics/models.py
# Amy Ho, aho@bu.edu
from django.db import models
from datetime import datetime
import csv

# Create your models here.

class Voter(models.Model):
    '''Represents a registered voter.'''

    # identification
    last_name = models.TextField()
    first_name = models.TextField()

    # address 
    st_number = models.TextField()
    st_name = models.TextField()
    apt_num = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
 
    # dates
    doB = models.DateField()
    doReg = models.DateField()
 
    # voting info
    party_affiliation = models.CharField(max_length=2)
    precinct_num = models.CharField(max_length=10)
 
    # Election participation flags
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    
    # Calculated field
    voter_score = models.IntegerField(default=0)
 
    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} ({self.party_affiliation}, {self.doB}), {self.zip_code}'

def load_data():
    '''Function to load data records from CSSV file into the Django database.'''

    filename = 'data/newton_voters.csv'
    f = open(filename)
    f.readline()

    # read several rows
    for line in f:
        fields = line.strip().split(',')

        try:
            # create a new instance of Voter object with this record from csv
            voter = Voter(
                last_name=fields[1],
                first_name=fields[2],
                st_number=fields[3],
                st_name=fields[4],
                apt_num=fields[5] or None,
                zip_code=fields[6],
                doB=datetime.strptime(fields[7], '%Y-%m-%d').date(),
                doReg=datetime.strptime(fields[8], '%Y-%m-%d').date(),
                party_affiliation=fields[9],
                precinct_num=fields[10],
                v20state=fields[11].upper() == 'Y',
                v21town=fields[12].upper() == 'Y',
                v21primary=fields[13].upper() == 'Y',
                v22general=fields[14].upper() == 'Y',
                v23town=fields[15].upper() == 'Y',
                voter_score=int(fields[16]),

            )

            voter.save()
            print(f'Created voter: {voter}')

        except Exception as e:
            print(f'Skipped: {fields}')
            print(f'Error: {e}')
    print(f'Done. Created {len(Voter.objects.all())} voters.')