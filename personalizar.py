from pathlib import Path
import re

paginas = {
    "capoeira": ("Capoeira", "0x1769aa"),
    "jumping_down": ("Jumping Down", "0xd97706"),
    "praying": ("Praying", "0x16a085"),
    "sitting_laughing": ("Sitting Laughing", "0x8e44ad"),
    "taunt": ("Taunt", "0xc0392b"),
}

for nombre, (modelo, color) in paginas.items():
    archivo = Path("examples") / f"webgl_loader_fbx_{nombre}.html"
    codigo = archivo.read_text(encoding="utf-8")

    bloque = f"""
                                                        if ( child.material ) {{
                                                            const materiales = Array.isArray( child.material )
                                                                ? child.material
                                                                : [ child.material ];

                                                            materiales.forEach( ( material ) => {{
                                                                if ( material.color ) material.color.set( {color} );

                                                                if ( 'shininess' in material ) {{
                                                                    material.shininess = 80;
                                                                    if ( material.specular ) material.specular.set( 0xffffff );
                                                                }}

                                                                if ( 'roughness' in material ) material.roughness = 0.3;
                                                                if ( 'metalness' in material ) material.metalness = 0.45;

                                                                material.needsUpdate = true;
                                                            }} );
                                                        }}
"""

    patron = r"(child\.receiveShadow = true;)"
    codigo_nuevo, cambios = re.subn(
        patron,
        lambda coincidencia: coincidencia.group(1) + bloque,
        codigo,
        count=1
    )

    if cambios == 0:
        print(f"ERROR: {archivo.name}: no se encontró el punto de inserción")
    else:
        archivo.write_text(codigo_nuevo, encoding="utf-8")
        print(f"Material agregado: {archivo.name}")
