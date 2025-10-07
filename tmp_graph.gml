graph [
  directed 1
  node [
    id 0
    label "host:10.0.0.2"
    type "host"
  ]
  node [
    id 1
    label "host:10.0.0.5"
    type "host"
  ]
  node [
    id 2
    label "host:10.0.0.8"
    type "host"
  ]
  node [
    id 3
    label "host:192.168.1.4"
    type "host"
  ]
  node [
    id 4
    label "host:10.0.0.9"
    type "host"
  ]
  node [
    id 5
    label "host:10.0.0.10"
    type "host"
  ]
  edge [
    source 0
    target 0
    events "_networkx_list_start"
    events [
      action "unknown"
      ts "2025-10-01T09:00:00"
      user "alice"
      raw ""
    ]
  ]
  edge [
    source 0
    target 1
    events "_networkx_list_start"
    events [
      action "unknown"
      ts "2025-10-01T09:05:00"
      user "alice"
      raw ""
    ]
  ]
  edge [
    source 1
    target 1
    events "_networkx_list_start"
    events [
      action "unknown"
      ts "2025-10-01T09:07:00"
      user "alice"
      raw ""
    ]
  ]
  edge [
    source 1
    target 2
    events [
      action "unknown"
      ts "2025-10-01T09:10:00"
      user "alice"
      raw ""
    ]
    events [
      action "unknown"
      ts "2025-10-01T09:20:00"
      user "alice"
      raw ""
    ]
  ]
  edge [
    source 2
    target 2
    events "_networkx_list_start"
    events [
      action "unknown"
      ts "2025-10-01T09:22:00"
      user "alice"
      raw ""
    ]
  ]
  edge [
    source 2
    target 4
    events "_networkx_list_start"
    events [
      action "unknown"
      ts "2025-10-01T09:25:00"
      user "alice"
      raw ""
    ]
  ]
  edge [
    source 2
    target 5
    events "_networkx_list_start"
    events [
      action "unknown"
      ts "2025-10-01T09:30:00"
      user "alice"
      raw ""
    ]
  ]
  edge [
    source 3
    target 1
    events "_networkx_list_start"
    events [
      action "unknown"
      ts "2025-10-01T09:15:00"
      user "bob"
      raw ""
    ]
  ]
  edge [
    source 5
    target 5
    events "_networkx_list_start"
    events [
      action "unknown"
      ts "2025-10-01T09:35:00"
      user "alice"
      raw ""
    ]
  ]
]
