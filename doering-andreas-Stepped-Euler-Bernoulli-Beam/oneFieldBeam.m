%[text] Reference:
%[text] Static, Vibration Analysis and Sensitivity Analysis of Stepped Beams Using Singularity Functions 
%[text] by Peng Cheng, Carla Davila and Gene Hou
%[text] ![2supp.png](text:image:396a)
function [w,dw,ddw,M] = simpleSupportedBeam(x_val, E_val, L_val, dF_val, F_val, I_val, b_val,bc_left,bc_right)
%[text] **Input**
%[text] x\_val .. value for beam position in m
%[text] E\_val .. value for elastic modulus in N/m^2
%[text] L\_val .. value for beam length in m
%[text] d\_F\_val .. value for load position in m
%[text] F\_val .. value for load in N
%[text] I\_val=\[I\_1 I\_2\] .. value for second moment of area in m^4
%[text] b\_val=\[b\_1 b\_2\] .. values for region of inhomogeneity in m
%[text] bc\_left .. boundary condition left side ('pinned' or 'fixed'); default value is 'pinned'
%[text] bc\_right .. boundary condition left side ('pinned' or 'fixed'); default value is 'pinned'
%[text] 
%[text] **Output**
%[text] w .. displacement
%[text] dw .. first derivative of displacement (rotation)
%[text] ddw .. second derivative of displacement (curvature)
%[text] M .. bending moment
%[text] 
%[text] **Assumptions:**
%[text] $0 \\leq L$, $0\\leq E$, $0 \\leq I\_1$, $0 \\leq I\_2$
%[text] $0 \\leq x \\leq L\n$,  $0 \\leq d\_F \\leq L\n$
%[text] $0 \\leq b\_1 \< b\_2 \\leq L\n$
if ~exist('bc_left','var') || isempty(bc_left)
    bc_left='pinned';
end
if ~exist('bc_right','var') || isempty(bc_right)
    bc_right='pinned';
end

syms M x E L dF F
syms(sym('C_',[1 4])) % integration constants
syms(sym('R_',[1 2])) % support reaction
syms(sym('b_',[1 2])) % position of irregularity
syms(sym('I_',[1 2])) % second moment of area

sf_0(x) =   heaviside(x); % singularity function: step function
sf_1(x) = x*heaviside(x); % singularity function: integration of step function
%[text] support reaction
R_1_sub=(F*(L-dF))/L;
R_2_sub=(F*dF)/L;
%[text] Bending moment
M(x) = R_1*sf_1(x) - F*sf_1(x-dF) + R_2*sf_1(x-L) +C_1*x +C_2;
%[text] Reciprocal of moment of inertia 1/I(x)
invI(x) = 1/I_1 - (1/I_1-1/I_2)*sf_0(x-b_1) - (1/I_2-1/I_1)*sf_0(x-b_2);
%[text] Differential eq.
ddw(x)=M(x)*invI(x)/E;
ddw(x)=expand(ddw);
 dw(x)=int(ddw(x),x) + C_3;
  w(x)=int( dw(x),x) + C_4;
%[text] Boundary conditions
if strcmp(bc_left,'pinned')
    bc1= w(0)==0;
    bc2= M(0)==0;
elseif strcmp(bc_left,'fixed')
    bc1=  w(0)==0;
    bc2= dw(0)==0;
else
    error('Unknown boundary condition.')
end
if strcmp(bc_right,'pinned')
    bc3= w(L)==0;
    bc4= M(L)==0;
elseif strcmp(bc_right,'fixed')
    bc3=  w(L)==0;
    bc4= dw(L)==0;
else
    error('Unknown boundary condition.')
end

bc=[bc1 bc2 bc3 bc4];

zeroTerms=[heaviside(x-L) heaviside(dF-L) ...
          heaviside(-b_1) heaviside(-b_2) heaviside(-L) heaviside(-dF)  ...
          ];
bc=subs(bc,zeroTerms,zeros(size(zeroTerms)));

oneTerms=[heaviside(L) heaviside(L-x) heaviside(L-dF) ...
           sign(L-b_1) sign(L-b_2) sign(L) sign(b_1) sign(b_2) ...
           heaviside(b_1) heaviside(b_2) heaviside(x)];
bc=subs(bc,oneTerms,ones(size(oneTerms)));
%[text] Solve the diff. eq.
sol=solve(bc,[C_1 C_2 C_3 C_4]);
%[text] Substitute constants
ddw(x)=subs(ddw(x),sym('C_',[1 4]),struct2array(sol));
 dw(x)=subs( dw(x),sym('C_',[1 4]),struct2array(sol)); 
  w(x)=subs(  w(x),sym('C_',[1 4]),struct2array(sol));
  M(x)=subs(  M(x),sym('C_',[1 4]),struct2array(sol));
%[text] Substitute bearing reactions
ddw_val(x)=subs(ddw(x),sym('R_',[1 2]),[R_1_sub R_2_sub]);  
 dw_val(x)=subs( dw(x),sym('R_',[1 2]),[R_1_sub R_2_sub]);
  w_val(x)=subs(  w(x),sym('R_',[1 2]),[R_1_sub R_2_sub]);
  M_val(x)=subs(  M(x),sym('R_',[1 2]),[R_1_sub R_2_sub]);
%[text] Substitution of variables with values
vars=[F     dF       I_1      I_2      b_1      b_2      L     E];
vals=[F_val dF_val I_val(1) I_val(2) b_val(1) b_val(2) L_val E_val];

ddw(x)=subs(ddw_val(x),vars,vals);
 dw(x)=subs(dw_val(x),vars,vals);
  w(x)=subs(w_val(x),vars,vals);
  M(x)=subs(M_val(x),vars,vals);

ddw=subs(ddw(x),x,x_val);
 dw=subs( dw(x),x,x_val);
  w=subs(  w(x),x,x_val);
  M=subs(  M(x),x,x_val);

end

%[appendix]{"version":"1.0"}
%---
%[text:image:396a]
%   data: {"align":"baseline","height":261,"src":"data:image\/png;base64,iVBORw0KGgoAAAANSUhEUgAAA2EAAAHKCAYAAACKSEM7AAAylElEQVR42u3dDYhl12HY8cFSrZGp6UIgmULSCJykg5OmI4fSUWndaQvJlFKypYg+7LZZtzQZQj\/UJNhKQ6oSUpxAqA1u2UYh3X6lCrjEDUnZEFymtuvYEOjYTuMlsZNpE8TYa2lnV5a00ujj1mfkJ799e8999753733n3Pv7wSGxdmdn5n3e\/zvnnrtRAAAA0JsNNwEAAIAIAwAAEGEAAACIMAAAABEGAACACAMAABBhAAAAIgwAAAARBgAAIMIAAAAQYQAAACIMAABAhAEAACDCAAAARBgAAAAiDAAAQIQBAAAgwgAAAEQYAACACAMAAECEAQAAiDAAAABEGAAAgAgDAAAQYQAAAIgwAAAAEQYAAIAIAwAAEGEAAACIMAAAABEGAAAgwgAAABBhAAAAIgwAAAARBgAAIMIAAABEGAAAACIMAABAhAEAACDCAAAARBgAAAAiDAAAQIQBAACIMAAAAEQYAACACAMAAECEMe\/q1avF3t7e+bhy5YobBAAARBhd2traKjY2Ns7H5uamGwQAAEQYnT4Avhpg0wEAAIgwRBgAAIgwRBgAACDCEGEAACDCSNPly5fvCLDJZOJGAQAAEUZXZndGDOP27dtuFAAAEGF0dudbiggAACIMEQYAACKMwZk\/H0yEAQCACKND8+eDiTAAABBhdHnHzwXYwcGBGwUAAEQYfUUYAAAgwhBhAAAgwsjf1atXRRgAAIgw+mJTDgAAEGEs4fT09HxDjQceeOCuqAoj\/PfJZFKcnJzceafblAMAAERYl5Gyt7dXGiO5\/277+\/ul8bUoyMyCAQCACOvEpUuX7oiNEGND\/d2axJgIAwAAEdaJCxcuDDI4wixY2e+2zAizY1Xfp2q546JljwAAwMgirCwYhmDZWbCycfv27U6+jzADAICRRViYxRlqhMVmwcLW88G1a9eK7e3tWrG0zPdpMoa0BBQAAERYhbCMbqgRFpt5KhOCbNkIa2u2DQAAGEGElc3ihN0Ehxphu7u7S8VU1xEWi0MAABBhQ\/vFSoLg8PBwEL\/b5uZm6e8XO\/9qmQiLLedsMsJFoadLJAEAgAFH2JDPBwvCeVZdLxV8xzveUfl1Yabx8uXL52H7xBNPeCYBAMCYI2zI54MF4Tyv2GxYWxF2\/\/33V37dlStXPHsAAECEvWbI54NNtTEbFkIutoTx3nvvrfzaMNsIAACIsNd+qQGfDzYVZsMWXUR5let52fEQAABE2EoRNkRNrgfWJMbqbMpRdZFnAABgRBE29E05Vgm2OjNnYZnjok05wvjYxz7m2QMAACKsKC5duiTCVgyx++67b+HW8x\/96EcHfVuFmA8bvITbK7ZkEwAARFhRvimHCLszxKqWMHZ5nlnuMR9mCQEAQITN\/0KRKGBxjE0vrtzWNchyjpZwW4h5AABE2JIRtru7655e8TZs+zpkqYtdAgAAAETYnNhFjOk\/wnKegQwzhR5HAACIsBrMYKQRYdOljUO7HWzOAQCACJtjBqOb+HA72JwDAAARJiLcfp2KLW01GwYAgAgTEa2655573H5FfGmr2TAAAERYjQgze1HfvffeK8KK15a22ugF0hUuqB4+FPH6DoAISzTCUpi9OD09PT9oqHtB5HVd9LgsPMbKRi+Q\/mv9zs6OEANAhK1bbPZiiKOLUJsPjzFf7NpGL5B+hM3GGACIsDWJzV6MbSwbaCE8tre3B7PVfNsHeiIMRBgAiLCSiBBh651NG3qEua1g\/cqWdntuAiDCEjtwNkRbW48lOyRCGso+dAszYs4TA0CEibA7xu7ubnF4eFh5UDFdDmisPw7tkAhpi2125MMSAERYAhE2NEdHR8X+\/r4A6zjsLly4IMIgYeGDq1iIAYAIE2G9HZCYSet+ACIMAESYCGvMbJoIg6amF0kOy39TDzHnhQEgwkRY1syweTwxXpcuXTof63weTC94P43Auq\/9QgwAESbCGEgcwliE+AnnRpadH9l3CC763jboAECEiTAGHHYwBmWzX2HZ36Joe9e73tX6Bx51noOx60QeHx+7MwEQYSIMjydIX9ns19WrV6PxFUbb55k2ibAgXFZi\/tISISYBQIQ5aMbjCUSYCANAhDloBo8n+FpUNXnsxzbvWGVsbW01jrBwDlgYs383RBkAiDAHzXg8QdJiQRUTgimMLgKsSYSF88LKzusEABHmoBmPJ8jucV+1Kcc0fu65557WnyvLbo\/vOQuACHPQjMcTZP24j50PFkzPCWuyk2Jdy26P7zkLgAhz0Eym5k\/y93hChIkwABBhIowOzZ\/k39aBJaSmbHfDuo\/3Ll93l\/235z9AAQAR1uFBhAijTbMn+YfNAqpmAyBnZede1X28pxhh8x+gAIAI68jBwYEIA2oJH9qE14ww29Pm1uptjvCzTSaT4uTkpPPbYn7ZX\/jfbYfS9IOy6e\/VZYSFD1C8DwAgwnpQdu5AWF4DTb1661bx3I\/+ePHMw+8snv3BR4pXrl93o4iuLEedkJufBQuvpU1mfWOhFG7zqtu7ywib\/1oAEGFd\/VIlb9aHh4fubRp79ofeUzz9jd\/y+ggxhuDKeYTleXVfO5uIrUCoM0QYACJsoBEGTYVZsBtvfdsdERYGwiv3IcIAQISJMJI0PwsmwoTXUJYldhFhZcvA64yw0Y0IA0CEDeBgTITRhrJZMBGWprId\/ZYNgpR2vpzdlbOP32+V181VAkuEASDCMmdnRNpSFmCnD+25YRLRxuyXyw10G2Fd\/mwiDAARlhA7I9JlhJ0dfsQNk0iAzV9QuGrs7u7anEeEiTAARFhfBxF2RqTNCGP98dVk9stMlwgTYQCIsDVFGIiwYQRY3dmvqs0nEGEAIMJEGCKMFgPM7JcIm3\/seD8AQISJMEQYLQdYOBdUeOUXYdPlpZPJpDg5OenktX3+sQMAIkyEIcKoODivc+6Xma98I2z20gJ7e9U7j5Y9FhaF26q\/EwCIMBFGj169dUuErVGd636Z\/UorwkJErXods2W+x6KY914AgAgTYaMLmed+9MfPr60VxrM\/+EjxyvXrWfzsz\/7Qe0TYGkxnwDY3NwWYCBNhAIgwEUYbIXP64ENZxNiNt75NhK0hwOpsviHA0oywa9eurRRgdXa0DN8jBPpspFeZn1EFABEmwoZ\/UP2V4CoLmfMY+7NvL279+b9S3Lr4cJJRVvYz33hw153aUXw5\/ysNZTNNi87VqvvvVI0m92kIsTC2t7ejXxceU\/OzYHUvW1C2FBYARJgIy8YzD78zGmHLjr6WNZZ977PDj7hTO1Dn\/C\/X\/erHdKZp1dfQaSTNxnPfj6n5x9Wi0KtaCltnAxAAEGEiLAkvf+73ipt73916iIURAq\/vCKN94cA3LC80+5WOpuddpfqYmn9cLVK1FHaZ2UAAEGGs1Uv\/57OdxJgIyzu+Fi1BFF8iTIQBIMJEGCtoe1YsLEsUYfkG2KINOA4PD91QazK\/lDC319DYY2vRY3LVnRsBQIR58xx0jIUNP7o+P0uEdWfROWDO\/0rDdEYst\/uj6W6adQLM+wgAImyJCHNSdZrWca6XCFufOtcAs\/18OsKMWG5LQsuCatHPX2djGBEGgAhbIsKs50\/Tjbd8e7KxI8LaPzhetATROWCsKjyGmsZT2UysCANAhDUU+5Sd9MS2sBdhw7NotkF80Yb5TUXqLKWcf88Ij0XvIQCIsBXfhL2BpiucHybChm\/RNvTOAUOEASDCMhfOY\/AGmo8QNzdC5HzTt6714swirLsAu3jxoiWI9Pr6Hx5XdR9bs+E2jTbvIQCIsGV+KW+g+URYJL7qblPfVaCJsNXjq+o6YOKLlMItbMk\/+5j0HgKACBNhw46wFq4Z1sWOiiJsNYvOAXMdsDsdPf3S+cB7CAAizBsoWURYF4EkwpbnHLD69n79RrHxH79wx7j98qtuGO8hAIgwb6CkHWFhWaIIS0fVLJjrgM29Vs0FWBgf+oMX3DDeQwAQYd5A6TfCgrBz4s29714cYA8+VJwdfkSEJWDRxZhTOA\/s9MVXi\/0Pn94RPddurm8ZYFmEPfapL3swrVnZYxgARJgIG3yE+bnyC7CqizGnsgSxLHrWOfskwtK0zFb3ACDCRJgIE2G9yuVizLEIW1f4lP0s27\/8lAcUAIgwEYYIE2HVctmIIxZhVz7\/fFI\/DwAgwgYRYcfHx+5tESbCOhCWIuZyMeay4Hni+HavP8PsdvSxCLNDYr3HXTgHMSwdnEwmxcnJiRsFABG2TmUnVYflUogwEdb+gfDFixeTXoJ4\/nO++GrpdvCbv\/DFXn+O+Z\/hvb\/1rPPCljS\/BDbEGACIsDWaP6k6jBBmiDAR1u2B8HSETTqSek0oCbAw3vfZ51r9PmGGKyxtLLvw8ieun931\/a8++YIIW1LZElgAEGFrdO3aNeeFiTAR1rGqizIfHh4m83OWxc90nDz\/Sq2omoZVGCGQysb81ve7V59eGIJh2eEDv\/QlEbbMm5fXeABEmDdoRNiY4iucixM23Eh5I46zr\/TV7956ORpgi5Yixr6uyagKsOmfh+ASYV7jARBh3qDJNnZu\/5ufFWEdq9qOPpWNOF565dXiO3\/lqWj81NmQo60Iq5qJi0VY2Kbe5hzNX+NtzgGACBNh1HDjLd9uJiwjVUsQU1qGOPnozdJlfnVnwcKyw7YiLJx31jTC1nkB6Zxf423OAYAIW\/OBogjLwzMPv\/OO0Dl9KI2DKBFW\/ryK7YSY0jLEF155tdj64PXiv\/6\/29EAWzQLVhVOdcc09GKRNf1zOyQup2wXXK\/zAIiwNYotlyI9L3\/u94qbe9\/9WoA9+FBxdvgREZZogO3s7GRzPbDYMsQQPos244gtH\/xr\/+Nm8ROffja6Mcd0zP\/7ZRH26P\/+WmDZnGPJ+7hkF1xLEgEQYWsUWy4FImy5AKuaAUtpJ8TXX9iW3A0xFk1hhB0Sl1Fn4w2bczQX2wXXkkQARNi6fqmEl0ohwnILsHDNr9SXINaNsGWjqc4MWooRFi5SffDJZyrPjwt\/Fs6hW\/b3W6fYkkSzYQCIsEQiLKWlUoiwXOSwE+K82Plcs0sAV42m6fXDZq8Jdu3mS71HWJ3Iqjt2fvXp7EIstiQxLJ0VYgCIsAQiDERYc7GlvSnPLK+6nHBREM1flHnRtvJdRtilj99qZRfHXEMsLEmMzYYJMQBEmAhDhGVlekHmsudSCLOUZ5YXbYRR5e4NPb7YKGLmwym2yUdbERZ2gWwzwnIMsdhsmPPDABBhIgwRlpWqZYipL+1d5fyqVQNm\/vvElka2FWFVF6MeS4iF2bAwMxt7vJoNA0CEiTBEWPIWXZA5dWVBE6Iids5WPMJOGl8XrM729GW7NC4bYeF3Cssg6\/x8Ydbs6pMv3PG1VeeSDSXELEsEQISJMERY8gGWwwWZm0bY9JytriIsdgHo2M9S5+\/1sUX9ohALM225cH4YACJMhCHCsgywqu3oU90NsW741NmivumyvUd+s\/wCzblEWJ0QG8r5YUIMABEmwhBhyak6DyzFCzLHhB0KY0FRtZV8WYStcn2wXCJsUYjlNhtWdX6YEANAhIkwRFgyqs4Dy\/FC51W7Bsa2ki+LsLq7KuYeYdMQC9FZ9vMef\/llIQYAIkyEcaeXj\/+vCFtBbBYs9e3oo1H54qvnSwVjIfahP3ihVoStGkI5RVgQ220xXI8sJ4tCLPzZ8fGxF04ARJgIIyVjirCqWbAcA2yqalliLHCahNDR04t3W8wtwmLLElddlpliiO3u7poRA0CEiTDa8uqtW8VzP\/rjxTMPv7N49gcfKV65fl2EVYjNguW4DHFe7GLJsU06yrZpr9roY9GGH7GvnZ2Ji80+rSPCpiGW+7lhdUMsbDYzmUzEGAAiTISxqmd\/6D13xFOIMREWN8RZsKqwahJhdUfMe3\/r2crAqorEdUVYEDs3LEchxLa3t6MhJsYAEGEijBbceOvb7gqoprNhY4mwsBRxqLNgU7Fd\/\/qIsHBx5KrAet9nn4v+m1c+\/\/zabrPY7FzOqravt2kHACJMhLGisoBqOhs2hgirujDzUGbBgrrnZS0bYWHWqErZbNg0wmKxU3bh5z7FliTmrM6M2OyHEGbGABBhIowGbrzl20sjqsls2BgiLHYuWLhg85DEIqxsm\/qqre3nwyvsvlhns4rwfeZn46ZfV2dmLez0ePDJZ+76NyYfvdnpZhlDi7Cpo6OjyouSmxkDQISJMJYQZr1WnQ0beoRV7YiY04WZV4mwsm3qQ\/CEJYJVMRb+vGn8zJ77NZ05C9+rToSF7eFjf6\/LzTKGGmGzMWZmDAARJsJoycuf+73obJgIe83BwcHgzwWbWrQ5RmmkfiWQwp\/PjxBgywpfG\/6NacDFliLORlqYAVv2fDQRttii3RNt4AGACBNhNBCbDau7JHHoEVY2CxYOMId0LthU2XLAde8+ePl34htyhEirmv0q+\/sibLUQqzsjNh1hkw8AEGEijDlhNmyVJYl1I2x6TbLTh\/bOx7LXJetTbEfEoS1DnBU2ukhp98HYronT0Lnwi+XLIUNMzm8f39WSxLFE2HyQNZkZs0wRABEmwpizygYddSNs\/ppky16XrM8Ai21KMHRl52Wl8vNMf6bproixQAvxVraMUYS1G2JmxgAQYSKMJa2yQUfdCCu7JlnKSxdjOyJ6jqRlNrTC7NddoTC3hbwI607YwGNzc3NhiJkNA0CEOcCkWG2DjjpfE5Yilv29sCwxVbEdEYe4IUfOQmRt\/\/JTr89+LYokEdZxFNe40LNNOwAYdYTFzndhnJbZoCMWV\/PKliKGcXb4kaw+oAhhNsQNOQb\/4i3C+ovihksUnSsGwOgiLLbcinFaZoOOWFzNh1puSxFjH1AIsPzMX2NMhPWrzsyYiz0DMKoIiy23YryabtBRJ65ioZbqUsQQYOGA0HMjb+G6YWXb7YuwfjWZGRNiAIwiwpzvwrymG3RUxdV0S\/pY2KW6FDF2ceawUyJpm160uSy+Yht3iLB+hE076sSY5YkAjDLCLLcat6YbdFTFVWwGLPVZsLIZ4rDj25CvDTYU+x8+rbxYc2zjDhHWjyazYmIMgFFFmDc8mmzQEYu1qvPAUp4Fi50n6cOJTF7TKgKsaoiw9QRZnYs9W6IIwCgizIU0iW3Qcet7\/vpdIRaLsCHNgjkXTISJsLRDLLxmASDCshG7qCbEliTOnxsWi7DYLNjpgw8lOQsWAiyc8+U8ybxNrxcmwvIKsTpLFM2IAYiwwQgXzBRhlIktSZw\/N6zsz3O8MHNsGaKliMMPsq0PXhdhmcSYEAMQYYNQdv0Wn\/oThOU9IZoWnRtW9udhR8SczgOrWobo+YAI6z\/GqpYoWjIPIMIG8WY3+8ljmBnzqT+zIbbo3LCyPy9bivjM3\/57yf6esVmwEGaeD4iw9ELMbBiACINBW3RuWGzJ4l2zYL\/xyWR\/x9gsmABDhKUZYmbDAEQYDFrVuWFlM2U3apxHlpKwFNEyRLqIsJPnX3HDtBBisQ2kzIYBiDAYrKpzw+ZnyW5UzISl6uDgwCxYIsJBdYjioUTY3q\/fcKe2oOzcZbNhACIseeGgJhxo1rkWy6IR\/o3JZOITyBGGWGxZYp2R23XBwlb10MTmL3zRksSOVO1cCjA2Vcf1Qz5O38jxjopd+2iV4RPI8alallgZYIleFyyIzYIdHh66w2kkzHqJsG7YuRRgueP6IUVZdhFW9QniqsOM2LhULUt8OsNliLGDO7NgLOPazZdEWFdvvHYuBVhpYmUIMbaR250V+wSxreHCmULsfHzTt2YXYbENOcyCsdTj6cVXRViPz1MBBoxNGxMr4VJUucbYxtjurLp1fXx87NkxohDL\/VywqucHLPV4+vgtEeZ5CtCZNidWcpxE2RjCnbXMJ4hhm+CqO393d9eM2IjU2aQjXLA51XPBqp4f0FSYBbvwi9dFmOcpQKuOjo6KK1euFO95z3tGv5otq1f+tk9kDg+E7e1tm3WwcJOOlDfjOD9odm0wWhSbBXvgl77kxknsfQwg9eB67LHHzscy539NhcmTqmP2HI\/ds4+wVdfRL7pT3\/\/+97\/+4AkPpPCAWvX7zT4gjf5G1f13vmX9W98WvXbY2W98Mu2D5sgSJ+eZsIzYLNjVJ19w4yT4PgYwhOCqu0pg0SSKCOvpzastsYtnxpYqLhMBXWytbzQfsfvvA\/\/wHxe\/86f\/zHl4Xf\/mP3n+f3\/7bbvF499\/sHLkdS2cmGqJE6291poFy\/J9DKDLsOr7+PbBBx+M\/mxhUiN2vWARltmbV7gzNzc3RYrRWeS1NWtX90MES5xYVtmFms2CtXTblrzPAPSl7oqsFCYOvu\/7vm\/h7yLC1hhhbe5i2GQ2zDDWGXTzkTa\/rDbMjFnixNKvhXMXajYLVnT2PuPDEqANdWatcluRFX7mZdpAhLUobDpwcHDQ+XbysaI2jFxn3da5RJKMPym9+VKx\/ctPnQfY1gevmwVr+VPo6QcmPiwBpq8Lq+wXMNTTXcJtIsLWbNH1wcKft+WNb3yjg3vDEskRBNzR0y8VVz7\/fPHYp77caPzAr32u+N5\/\/7HiL77\/V+4Y4b+FP1v09eF7hu8NbYledD6Taxz2PRswxM2lyPfxZ7+A8hGWbtfZbl6EdSy26cDsHdWWt7\/97R78htHyOW59jR\/4lx8ovvdn\/svCMNr\/8Gnp5hN9jt2rT4syB9ytjff\/k39afP47ynd4\/cNv\/VPFv\/v7\/2Dwt8FYDmZXfU0Wc928poipdscTTzxRL2REWLfqnKvV5pSwB79hJDj+xHcUG3\/hbxUbf+NHysePPLH2sFplfOPPffo8IENIDu3geD6Olxnzt82fm3x\/9eNhfoS\/Gx5DnkuG0eic47F8GCKiup\/ZeuSRR85v69iuhssc14uwHtbKLtq5sNUbpecHo9HtePTRR4sLFy54Ecx1vOmPZR9Yjcdj\/z3\/eJhGc9v3XbhtVvk3w9f\/8W\/xvDKMFmbchItR5xj3fe973x1LCz\/xiU8sXOVWR9gzQoQlMBtWZ93oKhEWHkBthkEIS\/oTHh8iL9Pxz35pXAFWJ8xSH6lH80\/\/LyFmGIbRweTBfHBVBdT02HrZkIrtGSHCOpgNq7o6doi0LiMM+oi8RZ8MjW685bvEl9FdiP2R+zzHDMMQVS2FVZvH3Yu+X4i4++67T4T1LbY0sa0HiAhjXWY\/GTLr9pXxl\/+uWDC6G9\/1Vx2MGYYxysBKaUVW2e+ws7NTeVz\/jne8I3rpKhG2hqWJbc2GiTByn3UbzIzad\/4loWB0N8LSSQdshmFkODu1rlmrLsRmtKZRNZlM7vidqmbBcrr2YpZ1UbWD4aqzELGLQkPZ4+Unf\/Ini5\/6qZ8qLl++XDz11FPZzKhlE3Bhudi\/+k2xYHQzwsYhDvwc0CY+LFMfz+NvrPsF1HmMT2Ms3EZVG8LkFKDZ1sWqSxKnwVVnm0wRRpnPfOYzo1wS2cX4sR\/7sfgyy3Be2Ac+k8iB+xfL\/\/t\/+kKx86tPFZc+fqv4F59+9vUR\/nf474InvXHvf3iy+OGf+Gk7yA505Dgb0PVrsk2k+ov4IT3++nh8v\/nNb27tflu0jFGEtSC2JDE8aS5evHjXtGWT4BJh0L\/KLWvDNvXf8\/297Oz3hr\/57uIb\/9H7i29+5APFN\/3wzxb3\/+tPRw\/kp+F19ckXK3+33z65Ufyd\/3BY\/NErvy+AEhibv\/DF4onj2550jE7VcvY2ZtyGMvsoovoT2+FwldHmZn0irETfF1UGhjkLF1sOcvT0S8Xer98oja4wy7UovMrcfPHV4n2ffa547FNfvmNsffC6OFoQTY\/85uq3Wfh3wteePP+KJxu0\/PorXFhGV7OzIqzDF4rYuVtdjJx2WgGWF8LryuefL\/Y\/fNpKdNV+TZuLs7ajrGyp5PyYXTpZ5+\/Hxr\/93eeL\/\/YHLxT\/8wtn5yP8\/+G\/1VmaWRZb4XYpi6bTSNDGRuzfAWB9x\/Ox4+5Fl6aajje84Q3Znhu2keMd1ucV2sP0fE47rQDNhYPz\/\/z7t18PiX\/+qWeLj18\/W9\/r3Exg1AmyqmhqGo9dh8ofPvfKHYH2c18JtF\/7ys\/4iS+dnc8UAjAOsaWIs8fdVTEWjtEff\/zxbJckbgzlDmsjtCxDBFJz++XiPFAOv\/Di+fiZ335upcgCgHULkyqxpYhNdX39YBH2VauuHa2a2cp9q0sAAEg9wGKr2pY5Bajr6wePPsKanAe27I2e8w4rAKTn7OzMjQAwo2pV2zKnAIUli7HZMBHW8R3W1o0euwOPj489YwAAYEWxVW2rbIQXmw0TYR3eYW1GWOwODAEIAAAsL7YjYjjOX2UjvNilq1I+rWgj5ztsemHAtiIs3IFlF3QO3wMAAFj+eD52LlgbO5HndlrRRs53WCzAVpl+zLGkAQAgZVWnFrUht10SN3K+w7q6M23QAQAA7eniXLBZue2SmHSEVV1DIPz3ru7MHHdYAQCAVI\/puzgXbFbVLokpzoZtpHxnxZYhVo027swcd1gBAIAUj+l3dnY6OxeszjF8irNhyZZF0y3p27wznRcGaTt75VU3AgBkoOo6v23L6ZphyUZY0y3p21xTen7DOC8MknTrTIABQA6qTi1q87h9Vmw2LLXJlI1U77B1LEOc5bwwAABYXmxl29bWVutLEadiK9pSm0zZyOkO6yvAcqpoAABITdUsWNdy2KBjI6c7rK8Ay6miAQAgNbFzwbpahjgrhw06koqwpjsidhVgOVU0AACkdkxfNqnS5TLEWTls0JFUhDVZhth1gOVS0QAAkFKAxSZVDg8Pe\/s5Ysfxk8kkiQmVjZTusLrLEPsIsFwqGgAAUg+wvo+fY6cWpTKhspHDHbaOacxFFQ0AAHxN1aq2Ps4FmxebTEnh9KKN1O+wEF19Tl3WrWgAAOA1Vava+lrFNi82mRLGzs7OWkMsiZpI7Q6760ayOQcAAETFJlXWeTwfJlO2t7eTDLG1Rlgo5tj2lWGkEGCxCLM5BwAAvCY2qZLC8XzVjNh0qWTfG3asNcJSWzcaY6t6AAC4W9WkSirH82FGLPwsi\/ae6HNmbK0RVrUbYiqzYFX1bDYMAIAxq5pUSel4vm6I9XV8v7YIC9WcwyzY9E6zVT0AANypalJleswfZsrqBFAqY9ARFqvmvregr8tW9QAAcKfYRMWb3\/zmrMJrFBFWtYXlOrejrxLbqt55YQAAjFXZRMX999+fZXwNPsKq1o6mLMVrDAAAwLrMbgM\/XdEW\/q8ISzDCYrNgqZ0LNi823WqDDgAAeM2iLeFTHn31SO8RVrUhR4rngtV9QJkNAwCA+EWSU9n7IYWfr9cICwG2v7+f5SzY9A6LnWBoNgwAAEgqwqoCLIdZsNkQs109AACQfIRVbcaRwyzYLNvVAwAAyUdYbDOO8N9zmQWbim1Xf3x87BEFAACsP8Jy3owjpmxJYpjtAwAAWHuExZYi5rYMcVbZksQQZnZJBAAA1h5hsaWIuc6CBbEliXZJBAAA1h5hZUv3cp4Fq\/q9XDMMAABYe4TNL93LcTOOOr\/XdOzs7AgxAABYo7AvxcHBQfQ6v2WTRJPJpJfj+F4ibPaq1KlcKbut3ys2G2ZZIgAAdB9P8xEVjtGX+fo+j+Nd3GpFsdkw1w0DAIDmAba\/v79UPLU5so6wqortc7qvS6G0Y5VtSSLAcNy+fbt48skn3RAAPXdD36OPvSs6jbDY1vSprMVsM8SG8rsAcLezs7Pi+PjYDQGIpAQiqcvR16lTnUZY+CVyutFXiabYuWFhfP3Xf70QAwAgW8tMrqQUVoeHh3f9TmWX0epLp9+p6nypsQ2zYgAA5GpdkytlM1NlQfimN72p8czWOvd06PQ7ze6KaNg1EQCAPPU9ubK7u1s6exWWRZbNYDUNqPDvDDbChJldEwEAyF9fx\/Cx+JqKLYtsuplG7N8ZbIQ1qdmhLksEAICxCMf773rXu4p777135eiJdUPTzTTamE3LOsK6rtDYVONsDPVV9kO6UDUAANQ5Fg\/X\/WrjmL\/OcX3tCFrzZMnaI6zLCq262NuqMdR0m04zYAAAjFUbx\/yxkGt6XB+LuT4nS9YaYW3WbJMAayPyFm3T+fjjj78+u2YGDACAMWvjmL+tyZt1nw+29ggLM0ldzVLt7Ox0OitVdR6bWS8AAPja6rFVj\/nbnLxZ9\/lga4uw6Z1RdoHjMHvVVdyFEW70NiLPeV8AAFB9vF916k6Tf+vixYutTd6kMImylgirWspXtSVl3TspVrdtBFjVz7\/qzw4AAEMIsKrTgppEWNW\/tezkzbrPB1tLhC3akr6rO7zNGaoUpjABACDXAKs789TF5E0Kx\/G9f8eqG3LVacCqf7vNB5bzwAAAoNnxeNPJkarJm2WPvWPH8oOOsKobso2ZqrbvpDJdbSbC19YO7+3tFZPJpDg5OXGjAABkdCxXteKt6fF+LOhWOcUohZ0Re42wqhPq2tqSvsvzwKoeWG1sJuJJe\/fUdYgxAADyPJZb9ni8ahO\/VSc\/UjmtqLfvGKvONmbAurwoc53fwYYc3d22AADkeyy3zPF4l6cvlYXdOk4r6uUot2pqso2A6etcMBtydMdtCwAwvGO5poGzaEnjqhMsYaVVV6vmkouwWCS1VZ19nAvW9e8wZjY7AQDIW1unBXU5CxZcu3at2N7eXvv1fXuJsPALdrlUsOtzwapCz4Yc3QWu2xYAIH2xD9SXOZaLdcM6gynbCJuf9mt7lqOPA\/hU1o8OkaWIAAD5avPc\/q67YVQRNjvt10XJlgVS1yG5rvWjQ2QpIgBAvmKzVyl2w6girGvzgdTFAXwq60fHEmFuXwCAPI\/FfaA+kggTSPlK5arlAACsfizueHxEEUa+XB8MAAARBj2yKUf+jo+P3QgAACKMbB6ANuUYtbAc9eDg4Hwt+WQyKU5OTtwoAIAIg74jzBri8ZhfjhpiDABAhEHPEcZ4lC1HBQAQYbDmCJsuWQvLFOeXLVrCJsIBAEQYtHAQHguvsmEJmwgDABBhsMJBeJ3wcuAuwgAARBi0dBC+zKgyO6tmCaMIAwAQYR2w7XU+91EfEVZ2QWhLGEUYAIAIa5Ftr\/O7j+qOra2tRgfuIfZcEFqEAQCIsI7Z9jrP+6gqvGavHbbKjooeEyIMAECEObBz8B0ZsYs2l\/3dJrspekx4rgIAiDAHdqOzubm5dCSV\/d1lljfiuQoAIMIc2I1GOE+vKpDCjFaT+7fJ8kaPCc9VAAAR5sBudK5du1a5dPDKlSt3\/P1Fyw3rzKx5THiuAgCIMAd2ow+xZeKpbFTNrDXdURHPVQAAEebAbrAWLUusO0LQbW9vl+6m6DHhuQoAIMIc2PFVi5Yl1hlV5495TKQrLDF1vwAAIkyEkVmIlc16eUzkIbajJQCACBNh9BRi0+WEbYWXx0TaYjtaMi7PP\/+8GwEAESbC8JhgXfdJnaWlDMfZ2ZkbAQAR5oAbEcY675OmM5wAACLMATeJKtsKH89TAAAR1uHB3fySp8lkUpycnHgEjMT8VviWvS1v0YWz6+5oKcIAABE2oggTZeOz6DpitBdYqwwAABE2kggTaowxeFIcAAAiTIQJM6EklEQYAIAISyXCRJvQMkQYAIAIK+K7rjW5IPBYx5BDUWy1P1Y5v06EAQAibAQRNk+UDSP2xFX7Y3d3tzg8PEzieQoAIMISFw7I2z64Ozo6Kvb39x2cG0nOKA39wxIAABGWuEuXLnV+cGcGTSghwgAARNhXXbhwIcmDO7NpQgsRBgAwyAiLnX9EtTHN7vVxvhPVulg2vOzPEc4n3Nvbs3MpACDC2jywM7Mxntgzk5WHPpYNL\/NzhBgDABBhGR7YAdVSWTZc9nMAAIiwDA\/sgAUvPIksG\/Z6AQCIsIEc2AHNn6vrWEYqwgAAETaQAzsgj\/gRYQCACHNABYOXys6IXjMAABHmgApGIWwJL8IAABEmwoCelG2gEy5k7jUDABBhIgzo6Xm6rotne80AAETYClI6zwRIP3xirxmzO6tOJpPi5OTEnZbIa3xYyhouqO1+AUCEJcKFmiEPm5uba3+ehgP6sASyKsKmY2dnxwF\/gq\/xIcYAQIStmQs1Qx7CwfO6r+UX+9AmNhzwp\/kaDwAibN2\/iAs1QxauXbtWbG9vnz9Ht7a21nItv9iHNlXDErj0XuMBQIQl+AbtQs1A3dcLM2IiDABEWAM25QDaiLAgzNSVnbc2HWbDRBgAiLDCphxAexEWzJ+3ZjZMhAGACJtjUw6gzQibPW\/Na4sIAwARVvPN2aYcwLIRNhWbEYuZXssqvP645pgIA4DRRZhNOYBVIyzMiNU9+K9z7TFLGUUYAAw6wgCaRljZTFWd15cmF382G+Z1HgBEGOCA\/qtjZ2fnrkha9PrSJMDMhnmdB4BBRJjt6YG2IqzumBXbnTWE2eHhYemfI8IAEGFZsz09sM4IK9udNQTYzZs3z\/\/89u3bXp9EGAAMK8JsTw80VXUx5qYRNv23vu3bvi362uP1SYQBwKAizPb0QFNVF2NeNOZfX9797ncXx8fH0e91+fJl8SDCAGD4EWZ7eqBK2Hp+\/lpedcbW1tZdry9nZ2eNAkw8iDAAGGSEAdQJse3t7WhcLSsWXtNzxapmzfBaD4AI88YMUENsgyDXCPNaDwAiDKADsQ2C5kfYKRGv9QAgwqAl4Zp1BwcHS51rNOYRbq\/JZJL1LFHd3RYfffTR878\/u2TxypUrnjxe6wEQYd6YQVgJtCaW3W3x677u64qf\/\/mf90TzWg+ACPPGjDAxxFsTs5t8NB1hFg2v9QCIMG\/MAskwxFpPURaer3itB0CEeWMWS4YhyDqOMpt0iDAARNig3piFjbHu0eZ1p4ZqlSV8zlcTYSIMABGW2BuzYbQ9dnd3i8PDQ68YPTo6Ojq\/uPFQZ9y+9KUvuZNFGAAiTIQZZnzIW26za+FnDT9zEGbUlo3OMczKiTAARJgIE0gg1pwnJ8IAYJwRVvciqZa5AYJsWMP5eACIsDWJXSQVQLQNe4TXfwAQYWs6IBJhgHgb5wAAEbauX8IbMzBSQ91Fsu45awAgwkQYQPZymbWz8RAAIkyEAeB1HgBEGABe57t2enpaHBwcnC+RHMN12wAQYSIMQISt1aVLl+76+XZ2doQYACIMAK\/zXdja2rKNPgAiDAAR1pfYNStdVBoAEQaA1\/kOhB0lw7lgsa30j4+P3YkAiDAAvM63HWKbm5ulP2s4ZwwARBgAXudbFluWGOLMskQARBgAXudbVnWha5t0ACDCAPA635HYskQAEGEAeJ3vQGxZoiWJAIgwALJQNrOUsrAs0ZJEAEQYANman1kK277nGI7enwAQYQBkYXbDi62treLq1avZhaP3JwBEGAB0HI7OCwNAhAHAmt+fnBcGgAgDgI44LwwAEQYAPXJeGAAiDAB6FDsvDAARJsIAwHsUACLMGxwA3qMA+JrT09Pi4ODgfLn3ZDLJdsdZEQYA3qMAsnDp0qVB7DgrwgDAexRAFi5cuDCI19Ts3wnClKQ3OAByijAXbAZo7zVVhK3B\/JSkCAMg9QMGF2wGaO81NccPtrKvlbIpSREGQCpcsBmg2wjL8YOtjSHeEQ888IBHKABJcMFmgPYM5YOtQUbY1atXPUIBSIILNgO0J\/bBVm5LEgcZYQCQ+nvVdOVGzte5Aehb7IOt3JYkDjLCcr94GwDjiLA+Dx6mFzgN4ScAgZwNYUniICPMJ40A5HDAkMKwUyOQmyGcazuKCMt1tBmP85+ADvF3BMjtgCGVAZCT2JLE4+NjESbCjLGFLkDVAcP29nayr4MAuSlbYRCuHyzCRJhhCD2gVCozY1tbW3YUBgbzOhrCTISJMMMwBC2UWvfMmPgChvA6mvPy6kFvUZ\/y8g\/DMEQZANBNB4gwN\/5SZd9VPO7u7haHh4eD\/h0NQ\/QBgAgTYW58RhS6hiHkAEAHiDAQeobAA4Cs1bnkUi7vgSIMELSG0GPQB2WG1wLG8\/zO5QL0IgwQZYaDQoSP4fnKYF5fRJgIA0SfYWR3UCqyDM8tcn3NyeUC9NkXS9nVsgFSdHR0VOzv7zsoMgzDEG6iq6MPenK5BmL2xTJ\/texc6hfATJ1hGIZAE1vLX3Te7oiJHHyEOyOX+gUwk2cYw7sOpg99DEHXTXyVHeeLMABwUDjK4QNQPF+FXlczXoteX0QYADDIg1KRheeWkeprjggDAADhZvT4QY8IAwCAgXNubFqz6iIMAACoZUwzbl0uaRZhAADA6EOvz\/NIRRgAAECfISPCAAAARJgIAwAARJgIAwAAEGEAAACIMAAAABEGAACACAMAABBhAAAADCnCwhW59\/b2iitXrrg3AQAAEda1ra2t8+0oNzc33ZsAAIAI6\/wXyPC6APRnOlN6+fJlNwYAACJMhNG1Bx544PXHx3vf+143CAAAIkyE0aVHHnnk9cdHWLLq3EEAAESYCKNDt2\/fPo8vIQYAgAgTYfQkLEOcfZwIMQAARJgIYw0hBgAAIkyE0WOIPfbYY24UAABEmAijS7MbdYQRdk+0NBEAABEmwuhI2Khjf3\/\/jsdN0xgL1x4Lf1\/AAQAgwqBmiF26dOmuEAvnidW5qPPstcecWwYAgAiDmubPEZudFauKsfmvcxFoAABEGLQQY1Ubd8xfBDomLF3c29uzbBEAABEGs2JLFGMhFv5+ncfe1taWZYsAAIgwqIqx+Y07YssNQ1hVxVqYBfP4BABAhEHDEIvNYs1vdz8bayHALly44PEJAIAImzo6Oio+9KEPnc9gXLx48Y4d7wxjfpTNhlXF2nQZ4nQcHBx4tQEAYHgRVmfMz04YRp0Rmw0LITa7LDHE2vwyRAEGAMCoI8wwlhn3339\/dIfD2WWJb3zjGy1DBABAhJWNnZ2d82WIYTliWJYYlifC1PxywiazYWbBAAAYTYQ54KUNIcybBlUIegEGAMDoIgxWEZYbzm\/QMplMan3tN3zDN9zxdffcc48bFAAAEQYxZbNfYefDsNSw6eNw0YWeAQAQYSKM0To9Pb3rel\/TGbC6ARZbvlh1oWcAAESYCGM0whbysevCNZn9Ci5fvnzH1z\/88MN3XTsstqsiAAAiTIQxyvBaNsCC2V0Up18\/v1tibFdFAABEmAhjsMq2nJ+OEGfLzFbNL0OcDbiwDNH5YQAAiDBGKcyCtX0Nr\/lliGW7KM6fa7a7u2tpIgAA+UfY7LIvKDM\/C9b2vxlbxhj+2+z5YZYmAgAwiAibLvtyYVzqhHpbj5PYMsSyEJv9\/j4sAADAESGD10WoN5mBnT0\/zIcFAACIMEgk7AAAEGEAAACIMAAAgHz9fzAtG6DBjJqUAAAAAElFTkSuQmCC","width":494}
%---
