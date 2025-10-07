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
  edge [
    source 0
    target 0
    events "_networkx_list_start"
    events [
      action "login"
      ts "2025-10-01T10:00:00"
      user "alice"
      raw "alice logged in successfully on 10.0.0.2"
    ]
  ]
  edge [
    source 0
    target 1
    events "_networkx_list_start"
    events [
      action "ssh_connect"
      ts "2025-10-01T10:05:00"
      user "alice"
      raw "ssh from 10.0.0.2 to 10.0.0.5 by alice"
    ]
  ]
  edge [
    source 0
    target 2
    events "_networkx_list_start"
    events [
      action "file_access"
      ts "2025-10-01T10:13:30"
      user "alice"
      raw "cat /etc/passwd on 10.0.0.8"
    ]
  ]
  edge [
    source 1
    target 2
    events "_networkx_list_start"
    events [
      action "privilege_escalation"
      ts "2025-10-01T10:07:00"
      user "alice"
      raw "sudo: alice used sudo on 10.0.0.8"
    ]
  ]
  edge [
    source 3
    target 1
    events "_networkx_list_start"
    events [
      action "login"
      ts "2025-10-01T10:12:00"
      user "bob"
      raw "failed login attempt for bob"
    ]
  ]
]
