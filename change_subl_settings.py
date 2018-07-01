#!/usr/bin/python

import os
import shutil
import sys
from termcolor import colored
from zipfile import ZipFile


class Theme_Changer():

    user_home = ''
    user_config = ''
    sub_dir = ''
    package_dir = ''
    pref_dir = ''
    user_config = ''
    theme_package = ''
    color_package = ''

    def __init__(self):
        self.get_paths()

    def get_paths(self):
        self.user_home = os.environ['HOME']
        self.sub_dir = self.user_home + '/.config/sublime-text-3/'
        self.package_dir = self.sub_dir + "Installed Packages/"
        self.pref_dir = self.sub_dir + 'Packages/User/'
        self.user_config = self.user_home + '/.config/sublime_preferences/'
        self.file_name = ''

    def validate(self):
        if not os.path.isdir(self.sub_dir):
            raise FileNotFoundError("Can't find sublime config directory in {}".format(self.sub_dir))
        if not os.path.isdir(self.package_dir):
            raise FileNotFoundError("Can't find sublime installed packages directory at {}".format(self.package_dir))
        if not os.path.isdir(self.pref_dir):
            raise FileNotFoundError("Can't find sublime user packages directory at {}".format(self.pref_dir))

        if not os.path.exists(self.user_config):
            ans = input("\nThere is not directory for your preferences.\nWould you like to create one in " + self.user_config + "? [Y\\n] ")
            if ans.startswith('y'):
                os.makedirs(self.user_config)

        settings_files = os.listdir(self.user_config)
        if settings_files == []:
            ans = input("\n\nNo files in your preferences directory.\nWould you like to copy over the default sublime preferences file? [Y\\n] ")
            if ans.startswith('y'):
                shutil.copyfile(self.pref_dir + 'Preferences.sublime-settings', self.user_config + 'Preferences.sublime-settings')

    def backup(self):
        # Copying the sublime preferences file to the current directory for safety
        shutil.copyfile(self.pref_dir + 'Preferences.sublime-settings', self.user_config + 'Old_Preferences.sublime-settings')

    def move_preferences(self, user_pref_file):
        # Copying new file to sublime preferences
        shutil.copyfile(user_pref_file, self.pref_dir + 'Preferences.sublime-settings')

        # Validate
        if os.path.isfile(self.pref_dir + 'Preferences.sublime-settings'):
            print(colored('Preferences Changed!', 'green'))
        else:
            print(self.error_message('Failed to change preferences'))

    def find_themes(self, package_dir):
        themes = {}

        packages = os.listdir(package_dir)
        for package in packages:
            contents = ZipFile(package_dir + package, 'r')
            contents = contents.namelist()
            for c in contents:
                if '.tmTheme' in c or '.sublime-theme' in c:
                    theme_name = package[:package.find('.')]
                    if theme_name not in themes:
                        themes[theme_name] = []

                    themes[theme_name].append(c)

        return themes

    def get_theme_settings(self, themes):
        os.system('clear')
        error = ''
        flag = True
        while flag:
            formatted_name = []
            curr = 1
            for theme, files in themes.items():
                print(theme + ':')
                for f in files:
                    formatted = str(curr) + '. ' + f
                    formatted_name.append(formatted)
                    print(formatted)
                    curr += 1

                print()

            if error != '':
                print(error)
                error = ''

            user_theme = input("Enter your new theme: ")
            user_color = input("Enter your new cholor scheme: ")

            for name in formatted_name:
                name_number = name[:name.find('.')]
                if name_number == user_theme:
                    user_theme = name[name.find('.') + 2:]

                if name_number == user_color:
                    user_color = name[name.find('.') + 2:]

            os.system('clear')
            flag = False
            if not user_theme.endswith('.sublime-theme'):
                error += self.error_message('Theme file must end with .sublime-theme!')
                flag = True
            if not user_color.endswith('.tmTheme'):
                error += self.error_message('Color scheme file must end with .tmTheme!')
                flag = True

        for key, value in themes.items():
            if user_theme in value:
                self.theme_package = key
            if user_color in value:
                self.color_package = key

        return (user_theme, user_color)

    def get_new_pref_file(self):
        os.system('clear')
        settings_files = os.listdir(self.user_config)
        print('Found {} files in {}'.format(len(settings_files), self.user_config))
        settings_files = os.listdir(self.user_config)
        curr = 1
        formatted_name = []
        for f in settings_files:
            formatted = str(curr) + '. ' + f
            formatted_name.append(formatted)
            print(formatted)
            curr += 1

        user_file = input("\nEnter the file you would like to use for your preferences: ")

        for name in formatted_name:
            name_number = name[:name.find('.')]
            if name_number == user_file:
                user_file = name[name.find('.') + 2:]

        return self.user_config + user_file

    def update_user_pref_file(self, user_pref_file, themes):
        ans = input("Would you like to change the theme and color scheme of the preference file? [Y\\n] ")
        if not ans.startswith('y'):
            return

        user_theme, user_color = self.get_theme_settings(themes)

        with open(user_pref_file, mode='r+') as file:
            old_pref = file.readlines()
            file.seek(0)
            file.truncate()  # clears file contents
            file.seek(0)
            for line in old_pref:
                if '\"color_scheme\"' in line:
                    continue
                elif '\"theme\"' in line:
                    continue
                elif '{' in line:
                    file.write(line)
                    file.write('\t\"theme\": \"' + user_theme + '\",\n')
                    file.write('\t\"color_scheme\": \"Packages/' + self.color_package + '/' + user_color + '\",\n')
                else:
                    file.write(line)

    def error_message(self, msg):
        return colored('\nError: ', 'red') + msg


theme_changer = Theme_Changer()
theme_changer.validate()
themes = theme_changer.find_themes(theme_changer.package_dir)
user_pref_file = theme_changer.get_new_pref_file()
theme_changer.update_user_pref_file(user_pref_file, themes)
theme_changer.backup()
theme_changer.move_preferences(user_pref_file)
