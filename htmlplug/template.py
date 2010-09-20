HEADER = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"> 
  <head> 
    <meta http-equiv="Content-type" content="text/html;charset=UTF-8" /> 
    <title>Tests report</title> 
    <style type="text/css" media="screen"> 
      a
      {
        color: #3d707a;
      }
      
      a:hover, a:active
      {
        color: #bf7d18;
      }
    
      body
      {
        font-family: "Lucida Sans Unicode", "Lucida Grande", sans-serif;
        font-size: 13px;
      }
 
      tr:hover
      {
        background: #f5f5f5;
      }
      
      #content-header
      {
        margin-left: 50px;
      }
 
      #content-header h1
      {
        font-size: 18px;
        margin-bottom: 0;
      }
 
      #content-header p
      {
        font-size: 13px;
        margin: 0;
        color: #909090;
      }
      
      pre {
        overflow: auto;
        width: 800px;
        text-align: left;
      }

      #result-list table
      {
        font-size: 13px;
        background: white;
        margin: 15px 50px;
        width: 800px;
        border-collapse: collapse;
        text-align: right;
      }
 
      #result-list thead tr.last th,
      th.statements
      {
        border-bottom: 1px solid #6d5e48;
      }
      
      th.statements
      {
        text-align: center;
      }
 
      #result-list th
      {
        padding: 3px 12px;
        font-size: 14px;
        font-weight: normal;
        color: #937F61;
      }
 
      #result-list td
      {
        border-bottom: 1px solid #e0e0e0;
        color: #606060;
        padding: 6px 12px;
      }
      
      #result-list tfoot td
      {
        color: #937F61;
        font-weight: bold;
      }
 
      #result-list .normal
      {
        color: #609030;
      }
 
      #result-list .warning
      {
        color: #d0a000;
      }
 
      #result-list .critical
      {
        color: red;
      }
 
      #result-list .test-name
      {
        text-align: left;
      }
      
      .footer-link
      {
        margin-left: 62px;
      }
   </style> 
  </head> 
 
  <body> 
"""
TITLE = """ 
<div id="content-header"> 
  <h1>Tests Report</h1> 
  <p>Generated: %s</p> 
</div> 
"""
TABLE_HEADER = """
<div id="result-list"> 
  <table> 
    <thead> 
      <tr class="last"> 
        <th class="test-name">Test</th> 
        <th>Result</th> 
      </tr> 
    </thead> 
    <tbody> 
"""
TABLE_ROW_NAME = """
<tr> 
  <td class="test-name">%s</td> 
"""
TABLE_ROW_FAIL = """
  <td class="critical">%s</td> 
</tr> 
"""
TABLE_ROW_OK = """
  <td class="normal">OK</td> 
</tr> 
"""
TABLE_ROW_TRACEBACK = """
<tr>
    <td colspan="2"><pre>%s</pre></td>
</tr>
"""
TABLE_FOOTER = """
    </tbody>
    <tfoot> 
      <tr> 
        <td class="test-name">
        Ran %s tests in %.4f sec<br/>
        Errors: %s, Failures: %s
        </td>
        <td>
            %s
        </td> 
      </tr> 
    </tfoot>
    </tbody> 
  </table> 
</div> 
"""
FOOTER = """
</body> 
</html> 
"""

