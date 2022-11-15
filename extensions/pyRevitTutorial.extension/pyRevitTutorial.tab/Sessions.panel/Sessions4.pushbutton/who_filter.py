from pyrevit import revit, DB, UI
from pyrevit import forms
from pyrevit import script

myconfig = script.get_config()


def who_created_selection():
    selection = revit.get_selection()
    if revit.doc.IsWorkshared:
        if selection and len(selection) == 1:
            eh = revit.query.get_history(selection.first)

            forms.alert('Creator: {0}\n'
                        'Current Owner: {1}\n'
                        'Last Changed By: {2}'.format(eh.creator,
                                                      eh.owner,
                                                      eh.last_changed_by))
        else:
            forms.alert('Exactly one element must be selected.')
    else:
        forms.alert('Model is not workshared.')


        options = {'Who Created Active View?': who_created_activeview,
           'Who Created Selected Element?': who_created_selection,
           'Who Reloaded Keynotes Last?': who_reloaded_keynotes}

selected_option = \
    forms.CommandSwitchWindow.show(options.keys())

if selected_option:
    options[selected_option]()



logger = script.get_logger()

with forms.WarningBar(title='Pick source object:'):
    source_face = revit.pick_face()


if source_face:
    material_id = source_face.MaterialElementId
    material = revit.doc.GetElement(material_id)

    logger.debug('Selected material id:%s name:%s', material.Id, material.Name)

    with forms.WarningBar(title='Pick faces to match materials:'):
        while True:
            try:
                dest_ref = \
                    revit.uidoc.Selection.PickObject(
                        UI.Selection.ObjectType.Face
                        )
            except Exception:
                break

            if not dest_ref:
                break

            dest_element = revit.doc.GetElement(dest_ref)
            dest_face = dest_element.GetGeometryObjectFromReference(dest_ref)

            with revit.Transaction('Match Painted Materials'):
                revit.doc.Paint(dest_element.Id,
                                dest_face,
                                material_id)


if my_config.get_option('proj_fill_color', True):
            to_style.SetSurfaceForegroundPatternColor(
                from_style.SurfaceForegroundPatternColor
                )