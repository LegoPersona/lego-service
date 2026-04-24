FROM fedora:36
COPY ./LPub3D-2.4.9.86.4133_20250319-1.fc36.x86_64.rpm ./LPub3D-2.4.9.86.4133_20250319-1.fc36.x86_64.rpm
RUN dnf install python3 -y; dnf install python3-pip -y
RUN dnf install util-linux -y; dnf install xorg-x11-server-Xvfb -y
RUN dnf install ./LPub3D-2.4.9.86.4133_20250319-1.fc36.x86_64.rpm -y
COPY src/ src
COPY templates/ templates
COPY requirements.txt .
RUN pip3 install -r requirements.txt
EXPOSE 8004
CMD ["uvicorn", "src.index:app", "--host", "0.0.0.0", "--port", "8004"]