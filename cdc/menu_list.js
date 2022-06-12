work = `
  <div class="menu">
    <nav>
      <ul class="nav-menu nav-center">
        <li><a href="#" class="nav-active">Home</a></li>
        <li><a>Homicide graphs</a>
          <ul>
            <li><a>Per 100K</a>
              <ul>
              <li><a href="#" onclick="change_graph('table0');">in california</a></li>
<li><a href="#" onclick="change_graph('table1');">all USA</a></li>
<li><a href="#" onclick="change_graph('table2');">under 18</a></li>
<li><a href="#" onclick="change_graph('table3');">over 18</a></li>
<li><a href="#" onclick="change_graph('table4');">by firearm in california</a></li>
<li><a href="#" onclick="change_graph('table5');">by firearm</a></li>
<li><a href="#" onclick="change_graph('table6');">under 18 by firearm</a></li>
<li><a href="#" onclick="change_graph('table7');">over 18 by firearm</a></li>

              </ul>
            </li>
            <li><a>All homicides</a>
              <ul>
              <li><a href="#" onclick="change_graph('table8');">in california</a></li>
<li><a href="#" onclick="change_graph('table9');">all USA</a></li>
<li><a href="#" onclick="change_graph('table10');">under 18</a></li>
<li><a href="#" onclick="change_graph('table11');">over 18</a></li>
<li><a href="#" onclick="change_graph('table12');">by firearms in california</a></li>
<li><a href="#" onclick="change_graph('table13');">by firearm</a></li>
<li><a href="#" onclick="change_graph('table14');">under 18 by firearms</a></li>
<li><a href="#" onclick="change_graph('table15');">over 18 by firearms</a></li>

              </ul>
            </li>
            <li><a name="uuuu">All homicides by age</a>
              <ul>
              <li><a href="#" onclick="change_graph('table16');">homicide</a></li>
<li><a href="#" onclick="change_graph('table17');">homicide per 100k</a></li>
<li><a href="#" onclick="change_graph('table18');">homicide by firearm</a></li>
<li><a href="#" onclick="change_graph('table19');">homicide per 100k by firearm</a></li>
<li><a href="#" onclick="change_graph('table20');">suicide per 100k by firearm</a></li>
<li><a href="#" onclick="change_graph('table21');">suicide by firearm</a></li>

              </ul>
            </li>
            <li><a>graphs with errors</a>
              <ul>
              
              </ul>
            </li>
          </ul>
        </li>
        <li><a href="#">Original CDC data</a>
          <ul>
          <li><a href="#" onclick="change_graph('table22');">original cdc california homicides</a></li>
<li><a href="#" onclick="change_graph('table23');">original cdc data homicides</a></li>
<li><a href="#" onclick="change_graph('table24');">original cdc data homicides under 18</a></li>
<li><a href="#" onclick="change_graph('table25');">original cdc homicide over 18</a></li>
<li><a href="#" onclick="change_graph('table26');">original cdc homicide over 18 by firearm</a></li>
<li><a href="#" onclick="change_graph('table27');">original cdc california homicides by firearms</a></li>
<li><a href="#" onclick="change_graph('table28');">original cdc data homicides by firearms</a></li>
<li><a href="#" onclick="change_graph('table29');">original cdc data homicides by firearms under 18</a></li>
<li><a href="#" onclick="change_graph('table30');">original cdc homicide by age</a></li>
<li><a href="#" onclick="change_graph('table31');">original cdc homicide by firearm by age</a></li>
<li><a href="#" onclick="change_graph('table32');">original cdc suicide by firearm by age</a></li>

          </ul>
        </li>
        <li><a href="#">Download spreadsheet</a>
          <ul>
            <li><a href="cdc_to_graph.py" target="__blank">cdc_to_graph.py</a>.</li>
          </ul>
        </li>
      </ul>
    </nav>
  </div>
`;
      load_menu_2(work);
      delete work;
      