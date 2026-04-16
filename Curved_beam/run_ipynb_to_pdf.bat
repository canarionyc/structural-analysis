call "C:\bat\Scripts_CMD\python_setup.bat"

rem jupyter nbconvert curved_beam_strippedout.ipynb --to latex --no-input --execute  --ExecutePreprocessor.skip_cells_with_tag=skip  --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags=skip
echo on
rem jupyter nbconvert curved_beam_strippedout.ipynb --to pdf --no-input --execute  --ExecutePreprocessor.skip_cells_with_tag=skip  --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags=skip

jupyter nbconvert  "Analisis de Cercha.ipynb" --to pdf --no-input --execute --ExecutePreprocessor.skip_cells_with_tag=skip --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags=skip --metadata "{\"title\": \"Analysis of Curved Beams\", \"authors\": [{\"name\": \"Tomas Gonzalez Llarena\"}]}"
