import json
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("Plotting stats for all files...")
    with open('classname_stats.json', 'r') as myfile:
        data=myfile.read()

        # parse file
        all_files_classnames_stats = json.loads(data)


        objects = tuple(all_files_classnames_stats.keys())
        y_pos = np.arange(len(all_files_classnames_stats))
        performance = all_files_classnames_stats.values()

        # plt.bar(y_pos, performance, align='center', alpha=0.5)
        # plt.xticks(y_pos, objects)
        # plt.ylabel('Count')
        plt.barh(y_pos, performance, align='center', alpha=0.5)
        plt.yticks(y_pos, objects)
        plt.xlabel('Count')
        plt.title('Classnames Count')

        plt.show()

if __name__ == "__main__":
    main()