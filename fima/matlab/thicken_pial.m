function thicken_pial(ribbon, hemi, sm_par, isoparm)
%THICKEN_PIAL make pial surface thicker, so that it better resembles a human brain
%
% Parameters
% ----------
% ribbon : str
%    path to the ribbon file (nii format)
% hemi : str
%    either l or r
% sm_par: [int, int] (only odd numbers)
%    degree of smoothing for 1) gaussian, 2) box smoothing
% isoparm : float
%    mesh connects the points that have this value
%
% Returns
% -------
% It writes file called lh.pial or rh.pial

addpath('/home/giovanni/tools/spm12')
addpath('/home/giovanni/tools/juniper/m-files/CTMR/MATLAB_scripts/Hermes2009/')
addpath('/home/giovanni/tools/freesurfer/matlab')

disp(ribbon)

surf = gen_cortex_click_from_FreeSurfer(ribbon, 'deleteme', isoparm, sm_par, hemi, '/tmp');
write_surf([hemi 'h.pial'], surf.vert, surf.tri)
