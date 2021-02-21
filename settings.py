from pathlib import Path

'''
Collection of paths which have been frequently used for  function testing.
Only required one is the 'RKI' path to the case number csvs.
'''

paths = {
    'RKI': Path('D:/Eigene Dokumente/Arbeit/Studium/Bachelorarbeit/Data/Robert-Koch-Institut/Covid Cases'),
    'movement_path': Path('D:/Eigene Dokumente/Arbeit/Studium/Bachelorarbeit/Data/Facebook/Germany Coronavirus Disease Prevention Map Mar 26 2020/Movement between Tiles'),
    'admin_movement_path': Path('D:/Eigene Dokumente/Arbeit/Studium/Bachelorarbeit/Data/Facebook/Germany Coronavirus Disease Prevention Map Mar 26 2020/Movement between Administrative Regions'),
    'population_path': Path('D:/Eigene Dokumente/Arbeit/Studium/Bachelorarbeit/Data/Facebook/Germany Coronavirus Disease Prevention Map Mar 26 2020/Facebook Population (Tile Level)'),
    'admin_population_path': Path('D:/Eigene Dokumente/Arbeit/Studium/Bachelorarbeit/Data/Facebook/Germany Coronavirus Disease Prevention Map Mar 26 2020/Facebook Population (Administrative Regions)'),
    'root': Path('D:/Eigene Dokumente/Arbeit/Studium/Bachelorarbeit/Graph Analysis'),
}