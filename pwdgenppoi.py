#! c:/Python27/python.exe
# -*- coding: utf-8 -*- 

import hashlib
import sys
import getpass
import os
import ConfigParser
import re

INI_FILE = os.path.join(os.path.dirname(__file__), "pwdgenppoi.config")
ini = ConfigParser.SafeConfigParser()

def nencode(num, chars):
  str = ""
  while num != 0:
    str = chars[num % len(chars)] + str
    num = (num - num % len(chars)) / len(chars)
  return str

# Code from
# http://blenderscripts.googlecode.com/svn-history/r41/trunk/scripts/sketch_export.py
def copy_to_clipboard(text):
       
        # =============================================================================
        # win32 (Windows)
        try:
            import win32clipboard
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text)
            win32clipboard.CloseClipboard()
            return True
        except:
            pass
       
        # =============================================================================
        # clip (Windows)
        try:
            import subprocess
            p = subprocess.Popen(['clip'], stdin=subprocess.PIPE)
            p.stdin.write(text)
            p.stdin.close()
            retcode = p.wait()
            return True
        except:
            pass
           
        # =============================================================================
        # pbcopy (Mac OS X)
        try:
            import subprocess
            p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            p.stdin.write(text)
            p.stdin.close()
            retcode = p.wait()
            return True
        except:
            pass
           
        # =============================================================================
        # xclip (Linux)
        try:
            import subprocess
            p = subprocess.Popen(['xclip', '-selection', 'c'], stdin=subprocess.PIPE)
            p.stdin.write(text)
            p.stdin.close()
            retcode = p.wait()
            return True
        except:
            pass
           
        # =============================================================================
        # xsel (Linux)
        try:
            import subprocess
            p = subprocess.Popen(['xsel'], stdin=subprocess.PIPE)
            p.stdin.write(text)
            p.stdin.close()
            retcode = p.wait()
            return True
        except:
            pass
           
        # =============================================================================
        # pygtk
        try:
            # Code from
            # http://www.vector-seven.com/2007/06/27/passing-data-between-gtk-applications-with-gtkclipboard/
            import pygtk
            pygtk.require('2.0')
            import gtk
            # get the clipboard
            clipboard = gtk.clipboard_get()
            # set the clipboard text data
            clipboard.set_text(text)
            # make our data available to other applications
            clipboard.store()
            return True
        except:
            pass
           
        return False


if __name__ == "__main__":

        ini.read(INI_FILE)
        
	print "enter masterkey (quit:q)"
	mkey_hash = hashlib.sha1(getpass.getpass()).hexdigest()
	if mkey_hash == "da39a3ee5e6b4b0d3255bfef95601890afd80709" or mkey_hash == "22ea1c649c82946aa6e479e1ffd321e4a318b1b0":
                print "otu"
		sys.exit()
	else:
                subkey = 0
                while subkey != "q":
                        print "enter subkey (config:c / quit:q)"
                	subkey = raw_input()
                	if subkey == "" or subkey == "q":
                                print "otu"
                		sys.exit()
                	elif subkey == "c":
                                print "config mode: subkey?"
                                subkey = raw_input()
                                print "config mode: how length? (must be in 4-16)"
                                try:
                                  key_info = int(input())
                                except:
                                  print "wrong parameter"
                                  break
                                if key_info < 4 or key_info > 16:
                                  print "wrong parameter"
                                  break
                                print "config mode: how type? (1. 09azAZSym / 2. 09azAZ / 3. 09az / 4. 09)"
                                try:
                                  key_info = str(key_info * 10 + int(input()))
                                  key_info = str(key_info.rjust(3,"0"))
                                except:
                                  print "wrong parameter"
                                  break
                                if int(key_info[2]) < 1 or int(key_info[2]) > 4:
                                  print "wrong parameter"
                                  break                                                                
                                ini.set('DEFAULT', str(hashlib.sha1(mkey_hash + subkey).hexdigest()), key_info)
                                f = open(INI_FILE, "w")
                                ini.write(f)
                                f.close()
                        if os.path.exists(INI_FILE):
                                try:
                                  key_length = int(ini.get('DEFAULT', str(hashlib.sha1(mkey_hash + subkey).hexdigest()))[0:2]) + 5
                                  key_type = int(ini.get('DEFAULT', str(hashlib.sha1(mkey_hash + subkey).hexdigest()))[2])
                                except:
                                  key_length = int(21)
                                  key_type = 1
                                finally:
                                  if key_type == 1:
                                    key_type = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJELMNOPQRSTUVWXYZ#$-=?@[]_'
                                  elif key_type == 2:
                                    key_type = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJELMNOPQRSTUVWXYZ'
                                  elif key_type == 3:
                                    key_type = '0123456789abcdefghijklmnopqrstuvwxyz'
                                  else:
                                    key_type = '0123456789'
                                  pwd = nencode(int(hashlib.md5(subkey).hexdigest(), 16) * int(mkey_hash, 16), key_type)
                                  pwd = pwd[5:key_length]
                                if re.search('[0-9]', pwd):
                                  pass
                                else:
                                  pwd = pwd[0:key_length - 6] + str(int(hashlib.md5(pwd).hexdigest(), 16))[5]
                        else:
                            key_type = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJELMNOPQRSTUVWXYZ#$-=?@[]_'
                            key_length = int(21)
                            pwd = nencode(int(hashlib.md5(subkey).hexdigest(), 16) * int(mkey_hash, 16), key_type)
                            pwd = pwd[5:key_length]
                            if re.search('[0-9]', pwd):
                                pass
                            else:
                                pwd = pwd[0:key_length - 6] + str(int(hashlib.md5(pwd).hexdigest(), 16))[5]
                	print "password generated: " + pwd
                        copy_to_clipboard(pwd)
