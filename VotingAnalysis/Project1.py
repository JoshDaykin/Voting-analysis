import sys
import csv
import time

# All possible options have uses here   
class Options:
    def __init__(self):
        self.data = self.load_csv_data("FullDataFor20241.csv")
        self.Constituency = Constituency(self.data)
        self.Members = Members(self.data)
        self.Parties = Parties(self.data)
        self.Region = Region(self.data)

    # Gives all methods access to the file once
    def load_csv_data(self, FullDataFor20241):
        data = []
        try:
            with open(FullDataFor20241, mode='r') as file:
                read = csv.DictReader(file)
                for row in read:
                    data.append(row)
        except FileNotFoundError:
            print("You must have the FullDataFor2024l in this folder")
        return data

    def display_title(self):
        print("=" * 50)
        print("United Kingdom party election results 2024 ".center(50))
        print("=" * 50)
        print("""
Searche abbreviations:
Conservative = con
labour = lab
Liberal Democrats = ld
reform UK = ruk
Green party = Green
Scottish national party = snp
Plaic Cymru = pc
Democratic Unionist Party = dup
Sinn Feinn = sf
Social Democratic and labour party = sdlp
Ulster Unionist Party = uup
Alliance Party Of Nothern Ireland = apni
""")          
        time.sleep(0.5)
        
# All options user can pick from
    def display_menu(self):
        while True:
            try:
            
                decide = int(input("""\nHow would you like to search?:
        1) Constituency
        2) MP's
        3) Parties
        4) Region
        5) Exit
        \nEnter here: """))
                if decide == 1:
                    self.Constituency.show_constituencies()
                elif decide == 2:
                    self.Members.show_members()
                elif decide == 3:
                    self.Parties.show_parties()
                elif decide == 4:
                    self.Region.show_region()
                elif decide == 5:
                    print("Exiting database...")
                    break
                else:
                    print("Please choose a valid option (1-6).")
            except ValueError:
                print("You must enter a number to continue")
            
class Constituency:
    def __init__(self, data):
        self.data = data
        
    def show_constituencies(self):
        """Search by constituency"""
        search_const = input("Type your constituency: ").strip().lower()
        found = False
        
        for row in self.data:
            """Makes search case unsensitive and collects all constituencies"""
            if search_const.lower() == row.get("Constituency name", "").strip().lower():
                
                party_member = row.get("Member first name", "N/A")
                party_member2 = row.get("Member surname", "N/A")
                print(f"\nSeat Winner: {party_member, party_member2}")
                
                winner = row.get("First party", "N/A")
                print(f"Winning Party: {winner}")
                
                """ All parties votes and their respective columns from CSV"""
                parties = [( "Labour Votes", "Lab"),
                           ("Conservative Votes", "Con"),
                           ("Liberal Democrats Votes", "LD"),
                           ("Reform UK Votes", "RUK"),
                           ("Green Party Votes", "Green"),
                           ("Scotland National Party Votes", "SNP"),
                           ("Plaid Cymru Votes", "PC"),
                           ("Democratic Unionist Party Votes", "DUP"),
                           ("Sinn Fein Votes", "SF"),
                           ("Social Democrates and Labour Party Votes", "SDLP"),
                           ("Ulster Unionst Party Votes", "UUP"),
                           ("Alliance Party of Northern Ireland Votes", "APNI"),
                           ("All Other Candidate Votes", "All other candidates")
                           ]
                for party_name, column in parties:
                    votes = row.get(column, "N/A")
                    if votes.isdigit() and int(votes) == 0:
                        continue
                    else:
                        print(f"\n{party_name}: {votes}")
                    time.sleep(0.5)

                found = True
                break
        if not found:
            print("That place doesn't exit")

class Members:
    def __init__(self, data):
        self.data = data
        
    def show_members(self):
        """Search by specific member"""
        search_person = input("Type the Mp's first name or surname:")
        found = False

        """Table headers"""
        print(f"\n{'MP Name:':<30}{'Party:':<10}{'Constituency:':<35}{'Result:':<10}")
        print("=" * 85)
        
        for row in self.data:
            """Gets the first and second name of all members"""
            first_name = row.get("Member first name", "N/A").strip().lower()
            surname = row.get("Member surname", "N/A").strip().lower()
            full_name = f"{first_name} {surname}"
            constituency = row.get("Constituency name").strip().lower()
            party = row.get("First party").strip().lower()
            result = row.get("Result").strip().lower()
            
            """Does the name match data in the file"""
            if search_person.lower() in first_name.lower() or search_person.lower() in surname.lower() or search_person.lower == full_name.lower():
                print(f"{full_name:<30}{party:<10}{constituency:<35}{result:<10}")
                time.sleep(1)
                found = True
                
        if not found:
            print(f"There is no MP by that name")


class Parties:
    def __init__(self, data):
        self.data = data
        
    def show_parties(self):
        """Search by party"""
        search_party = input("Which party?: ").strip().lower()
        total_votes = 0
        total_electorate = 0
        percentage = None
       

        """Gets the information from the parties column in CSV file"""
        votes = [
                    ("Con Total", "Con"),
                     ("Lab Total", "Lab"),
                     ("LD Total", "LD"),
                     ("RUK Total", "RUK"),
                     ("Green Total", "Green"),
                     ("SNP Total", "SNP"),
                     ("PC Total", "PC"),
                     ("DUP Total", "DUP"),
                     ("SF Total", "SF"),
                     ("SDLP Total", "SDLP"),
                     ("UUP Total", "UUP"),
                     ("APNI Total", "APNI"),
                     ("Everyone Else", "All other condidates")
                    ]
        
        """Percentage & total votes calc"""
        for row in self.data:
            electorate = row.get("Electorate", 0).strip()
            for party, key in votes:
               if search_party == key.lower():
                   vote_count = int(row.get(key, "0").strip())
                   total_votes += vote_count
                   total_electorate += int(electorate)
                   try:
                       percent = (total_votes / total_electorate)
                       percentage = "{:.1%}".format(percent)
                   except (ZeroDivisionError, UnboundLocalError):
                        print("That isn't a valid party")
                        return
            
            """Saves results of the search"""
        with open('Partypercent.txt', 'a') as file:
                  file.writelines(f"{search_party}: {percentage}\n")
                  
        print(f"Votes Received: {total_votes} Out of: {total_electorate}\nPercentage received: {percentage}")
        

class Region:
    def __init__(self, data):
        self.data = data
    def show_region(self):
        """Search by region"""
        search_region = input("What region?: ")
        found = False

        """Table Headers"""
        print(f"\n{'Constiuency:':<45}{'Region:':<45}")
        print("=" * 90)
        
        for row in self.data:
            """Gets all constituencies in region"""
            constituencies = row.get("Constituency name").strip().lower()
            region_name = row.get("Region name").strip().lower() 

            if search_region.lower() in region_name:
                print(f"{constituencies:<45}{region_name:<45}")
                time.sleep(0.5)
                found = True
                if not found:
                    print("That was not a valid region")
                    break
           


# This includes all the instances for options
menu = Options()
menu.display_title()
menu.display_menu()

