\
# EOD Report — NXCore Externals + SMB
**Generated:** 2025-11-04 02:55 UTC

This document captures exact commands used, current configurations, and a status roll‑up for the external SSD mounts and Samba exports on NXCore.

---

## Quick Reference: What Works
- **Windows mapping (as `glyph`):**
  ```powershell
  net use Z: \\\\100.115.9.61\\AeroDrive /user:glyph *
  net use X: \\\\100.115.9.61\\NXDrive   /user:glyph *
  ```
- **Shares:** `AeroDrive` → `/srv/AeroDrive`, `NXDrive` → `/srv/NXDrive`
- **Mounts:** `/dev/sdd1` → `/srv/AeroDrive` (UUID `3655-78FC`), `/dev/sde1` → `/srv/NXDrive` (UUID `5A00-F9C3`)
- **Group policy on mounts:** `gid=1006` (**AV-Share**) via `/etc/fstab` (no changes to `/home/glyph`)

---

## Completed
- Standardized to **single canonical paths**:
  - `/srv/AeroDrive` (SanDisk Extreme **Pro** 2TB, UUID `3655-78FC`, exFAT)
  - `/srv/NXDrive` (SanDisk **Extreme** 2TB, UUID `5A00-F9C3`, exFAT)
- Cleaned **Samba** config to only two shares (AeroDrive, NXDrive) restricted to `glyph`.
- Enabled **Tailscale IP** based mapping from Windows; verified `net use` works.
- Set **fstab** with `x-systemd.automount` + `_netdev` + `nofail`, using **UUIDs**.
- Ensured **AV-Share (GID 1006)** is applied to both mounts via `gid=1006` (does not touch glyph’s home).
- Resolved APT/DPKG prompt; kept local `lightdm-gtk-greeter.conf`.

## In Progress
- Optional **name-based** mapping (e.g., `\\\\nxcore\\AeroDrive`) pending DNS/hosts setup.
- Optional team write access by adding users to `AV-Share`.

## Planned
- (Optional) Purge GUI/greeter packages if headless long‑term:
  - `lightdm`, `lightdm-gtk-greeter`, X11 stack; set default target to `multi-user`.

---

## Exact Commands Used / To Repeat

### A. Identify Disks / UUIDs
```bash
ls -l /dev/disk/by-uuid/
ls -l /dev/disk/by-id/ | grep -E 'SanDisk|Extreme'
lsblk -o NAME,MODEL,SIZE,FSTYPE,MOUNTPOINT,UUID,TRAN,SERIAL
```

### B. Final Mount Points (one per device)
```bash
sudo mkdir -p /srv/AeroDrive /srv/NXDrive
# Unmount legacy locations (ignore errors if not mounted)
sudo umount -l /srv/disks/AeroDrive-2TB-fuse 2>/dev/null || true
sudo umount -l /srv/shares/AeroDrive/External-2TB 2>/dev/null || true
sudo umount -l /srv/backups 2>/dev/null || true
sudo umount -l /dev/sdd1 2>/dev/null || true
sudo umount -l /dev/sde1 2>/dev/null || true
```

### C. `/etc/fstab` (final lines)
```ini
UUID=3655-78FC  /srv/AeroDrive  exfat  uid=1000,gid=1006,fmask=0002,dmask=0002,iocharset=utf8,x-systemd.automount,nofail,_netdev  0  0
UUID=5A00-F9C3  /srv/NXDrive    exfat  uid=1000,gid=1006,fmask=0002,dmask=0002,iocharset=utf8,x-systemd.automount,nofail,_netdev  0  0
```

### D. Apply Mounts
```bash
sudo systemctl daemon-reload
sudo mount -a
# Trigger automounts
ls /srv/AeroDrive >/dev/null
ls /srv/NXDrive  >/dev/null
# Verify
mount | egrep '/srv/(AeroDrive|NXDrive)'
```

### E. exFAT Tooling & Health (read‑only checks)
```bash
sudo apt-get install -y exfatprogs
sudo fsck.exfat -n /dev/sdd1
sudo fsck.exfat -n /dev/sde1
```

### F. Samba Setup (shares for glyph)
```bash
# Set SMB password for glyph (separate from Linux login)
sudo smbpasswd -a glyph
sudo smbpasswd -e glyph

# Minimal smb.conf matching final layout:
# /etc/samba/smb.conf
[global]
   workgroup = WORKGROUP
   server role = standalone server
   disable netbios = yes
   smb ports = 445
   server min protocol = SMB2
   server max protocol = SMB3
   ntlm auth = ntlmv2-only
   map to guest = Bad User
   load printers = no
   printing = bsd

[AeroDrive]
   comment = AeroDrive (Apps, Music, AeroCoreOS assets)
   path = /srv/AeroDrive
   browseable = yes
   read only = no
   valid users = glyph
   force user = glyph
   create mask = 0664
   directory mask = 0775

[NXDrive]
   comment = NXDrive (Backups SSD)
   path = /srv/NXDrive
   browseable = yes
   read only = no
   valid users = glyph
   force user = glyph
   create mask = 0664
   directory mask = 0775
```

```bash
# Validate and restart Samba
testparm
sudo systemctl restart smbd
# Local verify without touching glyph’s home:
sudo -u glyph HOME=/tmp smbclient -L 127.0.0.1 -U glyph
```

### G. Windows Mapping (PowerShell)
```powershell
# Using Tailscale IP (works)
net use * /delete /y
net use Z: \\\\100.115.9.61\\AeroDrive /user:glyph *
net use X: \\\\100.115.9.61\\NXDrive   /user:glyph *
```

### H. Optional Headless Cleanup (not executed yet)
```bash
# Switch to non-GUI target and optionally purge greeter
sudo systemctl set-default multi-user.target
# sudo apt purge -y lightdm lightdm-gtk-greeter
# sudo apt autoremove -y
```

---

## Current Config Snapshots

### `/etc/fstab` (relevant)
```ini
UUID=3655-78FC  /srv/AeroDrive  exfat  uid=1000,gid=1006,fmask=0002,dmask=0002,iocharset=utf8,x-systemd.automount,nofail,_netdev  0  0
UUID=5A00-F9C3  /srv/NXDrive    exfat  uid=1000,gid=1006,fmask=0002,dmask=0002,iocharset=utf8,x-systemd.automount,nofail,_netdev  0  0
```

### `/etc/samba/smb.conf` (final)
```ini
[global]
   workgroup = WORKGROUP
   server role = standalone server
   disable netbios = yes
   smb ports = 445
   server min protocol = SMB2
   server max protocol = SMB3
   ntlm auth = ntlmv2-only
   map to guest = Bad User
   load printers = no
   printing = bsd

[AeroDrive]
   comment = AeroDrive (Apps, Music, AeroCoreOS assets)
   path = /srv/AeroDrive
   browseable = yes
   read only = no
   valid users = glyph
   force user = glyph
   create mask = 0664
   directory mask = 0775

[NXDrive]
   comment = NXDrive (Backups SSD)
   path = /srv/NXDrive
   browseable = yes
   read only = no
   valid users = glyph
   force user = glyph
   create mask = 0664
   directory mask = 0775
```

---

## Notes
- The `autofs` entries you see alongside the final mounts are expected due to `x-systemd.automount`.
- Using the **Tailscale IP** avoids potential hostname resolution issues in Windows.
- **No changes** were made to `/home/glyph` or its ACLs.

— End of report —
