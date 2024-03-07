

figure;
fig = gcf;
set(gcf,'color','white')
ax = gca(gcf);

color2 = "#75E6DA";%"#B00000";
color = "#29A0B1";%"#189AB4"; %"#0000FF";%1/255*[231,188,188];
color3 = "#05445E";
lw = 1.5;
bw = 0.5;

b = bar([12.2,11.2], 'EdgeColor','none'); hold on;
set(b(1), 'FaceColor',color, 'BarWidth', bw);