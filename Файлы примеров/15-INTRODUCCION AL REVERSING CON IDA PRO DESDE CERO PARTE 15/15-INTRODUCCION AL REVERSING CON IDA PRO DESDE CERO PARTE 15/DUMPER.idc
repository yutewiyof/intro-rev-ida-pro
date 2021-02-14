static main() 
{ 
auto fp, ea; 
fp = fopen("pepe.bin", "wb"); 
for ( ea=0x400000; ea < 0x40b200; ea++ ) 
  fputc(Byte(ea), fp); 
}
