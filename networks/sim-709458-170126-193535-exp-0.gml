graph [
  name "grid_2d_graph"
  node [
    id 0
    label "Onealbury"
    sw "L"
  ]
  node [
    id 1
    label "Hernandezfurt"
    sw "R"
  ]
  node [
    id 2
    label "Mccarthyfort"
    sw "R"
  ]
  node [
    id 3
    label "Dalemouth"
    sw "L"
  ]
  node [
    id 4
    label "Tiffanyton"
    sw "L"
  ]
  node [
    id 5
    label "West Luisfort"
    sw "L"
  ]
  edge [
    source 0
    target 3
    Onealbury "L"
    Dalemouth "L"
  ]
  edge [
    source 0
    target 2
    Onealbury "O"
    Mccarthyfort "L"
  ]
  edge [
    source 0
    target 4
    Onealbury "R"
    Tiffanyton "L"
  ]
  edge [
    source 1
    target 3
    Hernandezfurt "L"
    Dalemouth "O"
  ]
  edge [
    source 1
    target 2
    Hernandezfurt "R"
    Mccarthyfort "R"
  ]
  edge [
    source 1
    target 5
    Hernandezfurt "O"
