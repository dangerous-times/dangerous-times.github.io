option compatible
Global document   as object
Global dispatcher as object

Sub Main
	call load_homicide_sheets
End Sub

Sub load_homicide_sheets

   document   = ThisComponent.CurrentController.Frame
   dispatcher = createUnoService("com.sun.star.frame.DispatchHelper")

   REM ** Process the CSV file containing the spreadsheet list
   call loadCSV("cdc_csv_files", "cdc_csv_files", 0)

   REM ** Delete spreadsheets no longer needed
   ThisComponent.getSheets().removeByName("cdc_csv_files")
   ThisComponent.getSheets().removeByName("Sheet1")
   ThisComponent.getSheets().removeByName("Sheet2")
   ThisComponent.getSheets().removeByName("Sheet3")
   
   msgbox "done"
End Sub

Sub loadCSV(filename, sheetname, sheetNumber)
   cURL = convertToUrl( "C:\Users\xxxxx\python\homicide_files\work\" & filename & ".csv")

   REM ** Create sheet from CSV file **
   Const cFO = "9,34,76,1,,1033,false,true"       ' Sheet formatting options
   Const cFN = "Text - txt - csv (StarCalc)"
   xsh = ThisComponent.getSheets()
   if not xsh.hasByName(sheetname) then xsh.InsertNewByName(sheetname, sheetNumber)
   sh = xsh.getByName(sheetname)
   'globalscope.basiclibraries.loadlibrary("MRILib")
   'mri sh
   REM com.sun.star.sheet.XSheetLinkable
   sh.link(cUrl, cSheet, cFN, cFO, com.sun.star.sheet.SheetLinkMode.VALUE)  

   REM ** Original CDC files have the selection lines highlighted **
   if filename = "cdc_csv_files" then
      call processCSVFiles(sh)
   elseif instr(filename,"original") then
      call updateOriginalSheet(sh)
   else
      call updateSheet(sh, filename) 
   end if

End Sub

sub processCSVFiles(sheet)
   for sheetPosition = 0 to 1000
      filename = sheet.getCellByPosition(0, sheetPosition).getString()
      if filename = "" then exit for
      if left(filename,6) = "graph_" then
         sheetname = mid(filename,7)
      else
         sheetname = filename
      end if
      call loadCSV( filename, sheetname, sheetPosition )
   next
end sub

sub updateOriginalSheet(sheet)

   REM ** Find the start of the CDC selection criteria **
   for i = 0 to 10000
      if sheet.getCellByPosition(0, i).getString() = "---" then exit for
   next
   REM ** Highlight the CDC selection criteria **
   for i = i+1 to i+100
      if sheet.getCellByPosition(0, i).getString() = "---" then exit for
      sheet.getCellByPosition(0, i).cellbackcolor = rgb (255,255,0)
   next
   
end sub

sub updateSheet(sheet, filename)
 
   rem ** Make this the active sheet for UNO commands
   ThisComponent.getcurrentController.setActiveSheet(Sheet)
  
   for columns = 0 to 1000
      if sheet.getCellByPosition(columns,0).getString() = "" then exit for
   next
   columnLast = convertColumnNumberToName(columns) 
   
   for rows = 0 to 1000
      if left(sheet.getCellByPosition(0,rows).getString(),11) = "table_info " then exit for
   next
   rows = ltrim(rows)   'Remove leading blank from number

   REM ** verify the number of columns is correct for every line
   for i = 1 to int(rows)-1
      if sheet.getCellByPosition(columns,i).getString() <> "verify column" then
         msgbox "file " & sheet.name & ".csv invalid!" & vbCrLf & vbCrLf & _
            "Row " & i+1 & " missing 'verify column' after last column." & vbCrLf & vbCrLf & _
            "Aborting load for files."
         stop
      end if
   next

   REM ** delete verify column
   UNO( ".uno:GoToCell", _
         "ToPoint", "$" & convertColumnNumberToName( columns+1 ) & "1" _      
   )
   UNO( ".uno:DeleteColumns" )

   REM ** Sort the table
   UNO( ".uno:GoToCell", _
      "ToPoint", "$A$2:$" & columnLast & "$" & rows _
   )
   UNO( ".uno:DataSort", _
      "ByRows", true, _
      "HasHeader", false, _
      "CaseSensitive", false, _
      "IncludeAttribs", true, _
      "UserDefIndex", 0, _
      "Col1", 2, _
      "Ascending1", false, _
   )

   Dim LocalSettings As New com.sun.star.lang.Locale
   LocalSettings.Language = "en"
   LocalSettings.Country = "us"      
   NumberFormats = thisComponent.NumberFormats

   rem ** per 100K more readable when decimal point is aligned
   NumberFormatString = "#,##0.0"  
   per100kFormatId = NumberFormats.queryKey(NumberFormatString, LocalSettings, True)
   If per100kFormatId = -1 Then
      per100kFormatId = NumberFormats.addNew(NumberFormatString, LocalSettings)
   End If

   rem ** actual values more readable with comma for thousands
   NumberFormatString = "#,##0"  
   actualFormatId = NumberFormats.queryKey(NumberFormatString, LocalSettings, True)
   If actualFormatId = -1 Then
      actualFormatId = NumberFormats.addNew(NumberFormatString, LocalSettings)
   End If
   
   rem ** % Change values more readable with comma for thousands
   NumberFormatString = "#0%"  
   percentChangeFormatId = NumberFormats.queryKey(NumberFormatString, LocalSettings, True)
   If percentChangeFormatId = -1 Then
      percentChangeFormatId = NumberFormats.addNew(NumberFormatString, LocalSettings)
   End If

   rem ** Find the first PER 100K column
   for per100kStart = 0 to columns 
      if instr(sheet.getCellByPosition(per100kStart, 0).getString(), "per 100k") then exit for
   next
   per100kStart = per100kStart + 1       ' make the column number relative to 1 instead of 0
   
   rem ** Find the first actual column (ends the per 100k columns)
   for actualStart = per100kStart to columns 
      if instr(sheet.getCellByPosition(actualStart, 0).getString(), "actual") then exit for
   next            
   actualStart = actualStart + 1       ' make the column number relative to 1 instead of 0
   
   rem ** Find the first % change column if it exists (ends the actual columns)
   for percentChangeStart = actualStart to columns 
      if instr(sheet.getCellByPosition(percentChangeStart, 0).getString(), "%") then exit for
   next            
   percentChangeStart = percentChangeStart + 1       ' make the column number relative to 1 instead of 0
   if percentChangeStart > columns then percentChangeStart = columns + 1

   rem ** If per100k and actual columns next to each other, then alternating columns
   if (per100kStart+1) = actualStart then 
      for i = per100kStart to percentChangeStart-2 step 2
         UNO( ".uno:GoToCell", _
               "ToPoint", "$" & convertColumnNumberToName(i) & "$2:$" & convertColumnNumberToName(i) & "$" & rows _
         )
         UNO( ".uno:NumberFormatValue", _
            "NumberFormatValue", per100kFormatId       ' -1,000.0 formating' _
         )

         UNO( ".uno:GoToCell", _
               "ToPoint", "$" & convertColumnNumberToName(i+1) & "$2:$" & convertColumnNumberToName(i+1) & "$" & rows _
         ) 
         UNO( ".uno:NumberFormatValue", _
            "NumberFormatValue", actualFormatId       ' 1,000 formating' _
         )       
      next

   rem ** Otherwise actual columns follow per100k columns
   else
      UNO( ".uno:GoToCell", _
            "ToPoint", "$" & convertColumnNumberToName(per100kStart) & "$2:$" & convertColumnNumberToName(actualStart-1) & "$" & rows _
      )
      UNO( ".uno:NumberFormatValue", _
         "NumberFormatValue", per100kFormatId       ' -1,000.0 formating' _
      )

      UNO( ".uno:GoToCell", _
            "ToPoint", "$" & convertColumnNumberToName(actualStart) & "$2:$" & convertColumnNumberToName(percentChangeStart-1) & "$" & rows _
      )
      UNO( ".uno:NumberFormatValue", _
         "NumberFormatValue", actualFormatId       ' 1,000 formating' _
      )
   end if

   REM ** update % change format to %
   if percentChangeStart < columns then
      UNO( ".uno:GoToCell", _
            "ToPoint", "$" & convertColumnNumberToName(percentChangeStart) & "$2:$" & columnLast & "$" & rows _
      )
      UNO( ".uno:NumberFormatValue", _
         "NumberFormatValue", percentChangeFormatId       ' 1,000 formating' _
      )
   end if

   REM ** Create cell containing table info
   original_table_info = sheet.getCellByPosition(0, rows).getString()
   UNO( ".uno:GoToCell", _
      "ToPoint", "$a$" & int(rows)+1 _ 
   )
   UNO( ".uno:EnterString", _
      "StringName", original_table_info & _
            " data_rows='" & int(rows)-1 & "' data_start_per100k='" & int(per100kStart)-1 & _
            "' data_start_actual='" & int(actualStart)-1 & "' data_start_changed='" _
            & int(percentChangeStart)-1 & "'" _
      )

   REM **outline each cell in the first row (header)
   Cell = Sheet.getCellRangeByName( "$a$1:" & columnLast & "$1" )
   NewBorder = Cell.RightBorder
   NewBorder.OuterLineWidth = 88
   Cell.RightBorder = NewBorder
   NewBorder = Cell.TopBorder
   NewBorder.OuterLineWidth = 88
   Cell.topBorder = NewBorder
   NewBorder = Cell.BottomBorder
   NewBorder.OuterLineWidth = 88
   Cell.BottomBorder = NewBorder
   NewBorder = Cell.LeftBorder
   NewBorder.OuterLineWidth = 88
   Cell.LeftBorder = NewBorder

   REM **outline all other cells (not header)
   Cell = Sheet.getCellRangeByName( "$a$2:" & columnLast & "$" & rows)
   NewBorder = Cell.RightBorder
   NewBorder.OuterLineWidth = 20
   Cell.RightBorder = NewBorder
   NewBorder = Cell.TopBorder
   NewBorder.OuterLineWidth = 20
   Cell.topBorder = NewBorder
   NewBorder = Cell.BottomBorder
   NewBorder.OuterLineWidth = 20
   Cell.BottomBorder = NewBorder
   NewBorder = Cell.LeftBorder
   NewBorder.OuterLineWidth = 20
   Cell.LeftBorder = NewBorder

   REM **Center the header line   
   UNO( ".uno:GoToCell", _
         "ToPoint", "$a$1:" & columnLast & "$1" _
   )
   UNO( ".uno:HorizontalAlignment", _
      "HorizontalAlignment", com.sun.star.table.CellHoriJustify.CENTER _
   )

   REM ** Highlight the first 5 lines to default graphing to these rows.
   REM ** From OO Calc, you can manually change lines to be graphed by unhilie & hilite - color doesn't matter
   UNO( ".uno:GoToCell",  _
      "ToPoint", "$A$2:$" & columnLast & "$6" _
   )
   UNO(".uno:BackgroundPattern", _
      "BackgroundPattern.Transparent", false, _
      "BackgroundPattern.BackColor", 16777113, _
      "BackgroundPattern.URL", "", _
      "BackgroundPattern.Filtername", "", _
      "BackgroundPattern.Position", com.sun.star.style.GraphicLocation.NONE _ 
   )

   REM **delete sort column
   UNO( ".uno:GoToCell", _
         "ToPoint", "$b$1" _      
   )
   UNO( ".uno:DeleteColumns" )

end sub

Sub UNO(UNO_function, ParamArray arglist() As Variant) '**** As com.sun.star.beans.PropertyValue
   REM ** Create UNO arguments and execute it
   if UBound(arglist) = -1 then
         dispatcher.executeDispatch(document, UNO_function, "", 0, Array())
   else
      dim pArg((UBound(arglist)+1)/2-1) as new com.sun.star.beans.PropertyValue
      For i = 0 To UBound(arglist) step 2 
         pArg(i/2).Name = arglist(i)
         pArg(i/2).Value = arglist(i+1)
      Next 
      dispatcher.executeDispatch(document, UNO_function, "", 0, pArg)
   end if

   REM UNO = pArg   '****Function does not return anything - "AS" on SUB statement commented too
End Sub

sub convertColumnNumberToName(columnNumber) as string
   if columnNumber <= 26 then
      convertColumnNumberToName = mid("abcdefghijklmnopqrstuvwxyz", columnNumber, 1)
   else
      convertColumnNumberToName = mid("abcdefghijklmnopqrstuvwxyz", int((columnNumber-1)/26), 1) & _
         mid("zabcdefghijklmnopqrstuvwxy", (columnNumber mod 26)+1, 1)

   end if

end sub