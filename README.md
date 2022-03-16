# PyKlipd

## Summary

PyQt-based Clipboard Mananger for KDE environments.
Hooks all global Clipboard/Selection changes taking
ownership of current Clipboard/Selection contents.
This allows actual Clipboard/Selection stuff to be available
persistently in time (even if source application would have
been closed). Designed to be run as a daemon/service. Use
`pyklipd.desktop` in order to integrate the daemon into KDE
environment

## License

MIT License
