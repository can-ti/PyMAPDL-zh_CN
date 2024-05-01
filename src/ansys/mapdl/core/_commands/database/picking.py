# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
These DATABASE commands are generated by the GUI when picking
operations are performed.  They can also be used to add additional
parameters to a command.  For example, more points to a spline than
would be normally supported.
"""


class Picking:
    def fitem(self, nfield="", item="", itemy="", itemz="", **kwargs):
        """Identifies items chosen by a picking operation (GUI).

        APDL Command: FITEM

        Parameters
        ----------
        nfield
            Field number on the command which uses the picking data.  (Count
            the command name as a field, so that a 2 indicates the first
            command argument, 3 the second command argument, etc.)  The
            corresponding field on the command will have a P51X label.

        item
            Entity number of the entity picked.  Negative entity numbers are
            used to indicate a range of entities.  If the item picked is a
            coordinate location, then this field represents the X-coordinate.
            See also the FLST command.

        itemy, itemz
            Y and Z coordinates of a picked coordinate location.  ITEM
            represents the X coordinate.  See also the FLST  command.

        Notes
        -----
        This is a command generated by the GUI and will appear in the log file
        (Jobname.LOG) if graphical picking is used.  This command is not
        intended to be typed in directly in an ANSYS session (although it can
        be included in an input file for batch input or for use with the /INPUT
        command).

        On the log file, a set of FITEM commands is preceded by one FLST
        command which defines the picking specifications for that pick
        operation.  The data listed in the FITEM commands are used by the first
        subsequent command containing a P51X label in one of its fields.

        Caution:: : For a given entity type, a list containing an ITEM that is
        larger than the maximum defined entity, could deplete the system memory
        and produce unpredictable results.

        This command is valid in any processor.
        """
        command = "FITEM,%s,%s,%s,%s" % (
            str(nfield),
            str(item),
            str(itemy),
            str(itemz),
        )
        return self.run(command, **kwargs)

    def flst(self, nfield="", narg="", type_="", otype="", leng="", **kwargs):
        """Specifies data required for a picking operation (GUI).

        APDL Command: FLST

        Parameters
        ----------
        nfield
            Field number on the command which uses the picking data.  (Count
            the command name as a field, so that a 2 indicates the first
            command argument, 3 for the second command argument, etc.)  The
            corresponding field on the command will have a P51X label.

        narg
            Number of items in the picked list.

        type\\_
            Type of items picked:

            1
                Node numbers

            2
                Element numbers

            3
                Keypoint numbers

            4
                Line numbers

            5
                Area numbers

            6
                Volume numbers

            7
                Trace points

            8
                Coordinate locations (in Global Cartesian coordinates)

            9
                Screen picks (in X, Y screen coordinates (-1 to 1))

        otype
            Data order:

            NOOR
                Data is not ordered (default).

            ORDER
                Data is in an ordered list (such as for the E,P51X and A,P51X commands, in
                which the order of the data items is significant for the picking
                operation).

        leng
            Length of number of items describing the list (should equal NARG if
            Otype = NOOR; default).

        Notes
        -----
        Specifies data required for the FITEM command during a picking
        operation.  This is a command generated by the GUI and will appear in
        the log file (Jobname.LOG) if graphical picking is used.  This command
        is not intended to be typed in directly in an ANSYS session (although
        it can be included in an input file for batch input or for use with the
        /INPUT command).

        On the log file, FLST will always be followed by one or more FITEM
        commands which in turn are followed by the ANSYS command that contains
        a P51X label in one of its fields. This set of commands should not be
        edited.

        This command is valid in any processor.
        """
        command = "FLST,%s,%s,%s,%s,%s" % (
            str(nfield),
            str(narg),
            str(type_),
            str(otype),
            str(leng),
        )
        return self.run(command, **kwargs)