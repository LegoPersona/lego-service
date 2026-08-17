FROM fedora:36
COPY ./LPub3D-2.4.9.86.4133_20250319-1.fc36.x86_64.rpm ./LPub3D-2.4.9.86.4133_20250319-1.fc36.x86_64.rpm
RUN dnf install python3 -y; dnf install python3-pip -y
RUN dnf install util-linux -y; dnf install xorg-x11-server-Xvfb -y
RUN dnf install ./LPub3D-2.4.9.86.4133_20250319-1.fc36.x86_64.rpm -y
RUN mkdir -p "/root/.config/LPub3D Software"
COPY ["lpub3d24.conf", "/root/.config/LPub3D Software/lpub3d24.conf"]
COPY warmup.ldr /tmp/warmup.ldr
RUN xvfb-run -a env QT_OPENGL=software LIBGL_ALWAYS_SOFTWARE=1 \
    lpub3d24 -of /tmp/warmup_out.pdf -pe pdf /tmp/warmup.ldr \
    && rm -f /tmp/warmup.ldr /tmp/warmup_out.pdf \
    || echo "warmup done"
COPY src/ src
COPY requirements.txt .
RUN pip3 install -r requirements.txt
EXPOSE 8004
CMD ["uvicorn", "src.index:app", "--host", "0.0.0.0", "--port", "8004"]