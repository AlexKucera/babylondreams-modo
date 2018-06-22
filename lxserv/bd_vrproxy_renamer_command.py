#!/usr/bin/env python
# encoding: utf-8

"""

babylondreams - bd_vrproxy_renamer

Release Notes:

V0.1 Initial Release - 2018-06-22

Copyright 2017 - BabylonDreams - Alexander Kucera & Monika Kucera GbR

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


"""
 
import lx
import babylondreams
from bd_tools  import bd_vrproxy_renamer

class CommandClass(babylondreams.CommanderClass):

    def commander_execute(self, msg, flags):
        reload(bd_vrproxy_renamer)
        bd_vrproxy_renamer.main()

lx.bless(CommandClass, 'bd.vrproxy_renamer')
