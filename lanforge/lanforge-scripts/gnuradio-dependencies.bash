#!/bin/bash
files=(
    gr-osmosdr                        
    hackrf                            
    PyQt4                             
    PyQwt                             
    SDL                               
    SoapySDR                          
    airspyone_host                    
    boost-program-options             
    boost-serialization               
    codec2                            
    comedilib                         
    dbusmenu-qt                       
    fftw-libs-single                  
    flex                              
    freeglut                          
    gnuradio                          
    gr-fcdproplus                     
    gr-iqbal                          
    gsl                               
    hidapi                            
    jack-audio-connection-kit         
    kde-filesystem                    
    libffado                          
    libgfortran                       
    libmng                            
    libosmo-dsp                       
    libquadmath                       
    libsodium                         
    libxml++                          
    log4cpp                           
    log4cpp-devel                     
    openblas                          
    openblas-serial                   
    openblas-threads                  
    openpgm                           
    phonon                            
    portaudio                         
    python-rpm-macros                 
    python2-cheetah                   
    python2-devel                     
    python2-nose                      
    python2-numpy                     
    python2-numpy-f2py                
    python2-pyopengl                  
    python2-pyqt4-sip                 
    python2-rpm-macros                
    python2-scipy                     
    python2-sip                       
    python2-tkinter                   
    python2-wxpython                  
    python3-rpm-generators            
    qt                                
    qt-common                         
    qt-x11                            
    qwt                               
    qwt5-qt4                          
    rtl-sdr                           
    tix                               
    tk                                
    uhd                               
    wxGTK3-gl                         
    wxGTK3-media                      
    zeromq                            
    phonon-backend-gstreamer          
    sni-qt                            
)

#G=/var/tmp/deps_list.txt
#echo "" > $G
urls_file="urls_file.txt"
echo "" > $urls_file

while read L; do
   [[ x$L = x ]] && continue
   o=${L:0:1}
   o=${o,,}

   # where would be a logical place to see if the package has already been installed , use rpm -qa "$L"
   echo "https://archives.fedoraproject.org/pub/archive/fedora/linux/updates/30/Everything/x86_64/Packages/${o}/${L}.rpm"
done < deps_list.uniq.txt > $urls_file
exit

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
function f() {
   for f in "${files[@]}"; do 
         dnf repoquery --deplist --queryformat '%{name}.%{%arch}' "$f" \
         | grep 'provider:' \
         | sort | uniq \
         | grep -v '\.i686' \
         >> $G
      echo -n "."
   done 
}

