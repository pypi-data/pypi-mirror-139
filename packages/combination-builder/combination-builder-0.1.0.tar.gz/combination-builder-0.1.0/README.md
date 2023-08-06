# Echo Combination Builder #
A Python module for creating large-scale combination work list files.


## Summary ##
The intended purpose of this module is to provide a framework for easily constructing work list files for import to Echo acoustic liquid handlers (Beckman Coulter) that create combinations of substances for high throughput screening assays.  The original application was for small molecule screening, but additional applications should be possible without modification.  There are a series of steps involved in creating the work list files and this module provides the methods needed to perform these steps.


## Acknowledgement ##
If this software is helpful to you please acknowledge the source in your publications.  Please use the following acknowledgement:
"The authors would like to thank Duane Currier and Taosheng Chen of St Jude Children's Research Hospital for the use of the Combination Builder module (https://github.com/StJude-HTB/Echo-Combination-Builder)."


## Installation ##
**Dependency:** Python 3.8+

Install from pip:  
`python -m pip install combination-builder`  

## Use And Examples ##
From the Python prompt the following commands will import the example files and produce example outputs.  The examples files referenced below can be downloaded by cloning this repository or downloading them from the Example_Files directory.  
Import Combinations Module  
`import combination-builder as Combine`


### 1. Set Values and Initialize a Combinations Object ###
Set variables to indicate locations of input and output files:
Setting these variables here make setting all the variables easier since they are in one place, but the values can be substituted below in the actual calls to the methods if that is preferable.
The `map_filepath` is the path to the platemap file in either basic or 'Mosaic' format    
`map_filepath = "Example_Files\\ExamplePlatemap.txt"`  
  
The `concentration_file` is the path to the file containing assay concentrations for each substance  
`concentration_file = "Example_Files\\Example_Final_Concs.csv"`  
  
The `save_filepath` is the path where the Echo work list CSV file will be saved  
`save_filepath = "Example_Files\\ExampleOutput3.csv"`  
  
The `cmt_filepath` is the path where the Screener cmt mapping file will be saved  
`cmt_filepath = "Example_Files\\ExampleOutput4.cmt"`  
  
Set variables to control the locations of special wells:  
Setting `backfill_wells` here allows for easier reference to the well range to use for backfill wells.  Similar to the `control_wells`, `backfill_wells` is an array of well coordinates that can be extended or appended for discontinuous ranges.
`backfill_wells = Combine.generate_well_range("A21", "P24")`  
  
Setting `control_wells` here makes it easier to reference the well range later.  This range is an array of well coordinates that can be extended or appended for discontinuous ranges.  This is an exmple of creating two discontinuous control well ranges.  Please note that control substances are not currently handled by this module.  Use an alternate means to manually set control well transfers.
`control_wells = Combine.generate_well_range("A1","P2")`  
`control_wells.extend(Combine.generate_well_range("A13","P14"))`  

Set varaibles that specify assay conditions:  
Setting `static_transfer_volume` will force all transfers to be the same volume  
`static_transfer_volume = 100`  
  
Setting `assay_volume` is required and enables calculation of the assay concentration  
`assay_volume = 30`  
  
Setting `combination_max` is required and sets the maximum number of substances in each combination  
`combination_max = 3`  
  
Setting `substance_id_regex` is required and enables identification of the substance identifier in the plate map file  
`substance_id_regex = r'SJ[0-9-]+'`  

Initialize the object - This creates the bucket to store all the data in  
`exp = Combine.Combinations()`  

### 2. Load the plate map ###
Import the source plate map - were the source substances are on the source plate  
`exp.load_platemap(map_filepath, substance_id_regex)`  


### 3. Setup the backfill wells - Comment/Uncomment as needed
There are two ways to set the backfill source wells: manually create  
**Option 1:** Manually supply a list of wells this is fine for a small number of wells  
`wells = ["A21", "A22", "A23", "A24", "B21", "B22", "B23", "B24"]`  

**Option 2:** Generate well list from start and stop wells this option is good for a large number of wells list comprehension is required to get well alphas  
`wells = [x[0] for x in backfill_wells]`  

Set backfill wells is specific to individual plates  
Repeat for all plates with backfill wells  
`exp.platemap.plates["E3P00000776"].set_backfill_wells(wells)`  

### 4. Set up Combinations - Comment/Uncomment as needed
**Option 1:** Supply a manually curated list of combinations list compounds in separate columns, any number of columns is supported, header and any compound not in the platemap are skipped  
`combinations_filepath = "Combination Template.csv"`  
`exp.load_platemap(combinations_filepath)`  

**Option 2:** Calculate all permutations in the script specify how many compounds to include in each combination  
`exp.generate_combinations(combination_max)`  

### 5. Set transfer volume or assay conditions
**Option 1:** Set a static volume for all substances volume is in nanoliters - All combinations will be the 1:1:1 volume ratios  
`exp.set_transfer_volume(static_transfer_volume)`  

**Option 2:** Set assay volume and assay concentration assay volume is in microliters assay concentration(s) must be supplied  
`exp.set_assay_volume(assay_volume)`  
Set a constant concentration for all substances  
`exp.set_assay_concentration(conc=50, unit="mM")`  
Or set each concentration idependently with a csv file  
`exp.set_assay_concentration(file=concentration_file)`  

### 6. Configure assay plate layout
`exp.reserve_control_wells([w[0] for w in control_wells])`  

### 7. Create the transfer list
`exp.create_transfers()`  

### 8. Sort transfer list for optimized transfer speed
`exp.sort_transfers()`  

### 9. Save transfer list - Echo formatted CSV file
`exp.save_transfers(save_filepath)`  

### 10. Save *.cmt file - Screener Mapping File
**OPTIONAL** - Set replicate number to create replicate plates with the same plate mapping and concentrations  
`exp.save_cmt(cmt_filepath, 3)`  



**IN A NEW SESSION**  
This must be done after using the Echo CSV to transfer samples

### 11. Update CMT with barcodes after performing transfers
This is a new python session - initialize the module again  
`import Combinations as Combine`  

`cmt_filepath = "Example_Files\\ExampleOutput4.cmt"`  
`barcode_filepath = "Example_Files\\Barcode_List.csv"`  

Update barcodes  
`Combine.update_CMT_barcodes(cmt_filepath, barcode_filepath)` 