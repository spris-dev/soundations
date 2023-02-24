import joblib
import zipfile

from result import Ok, Err, Result
from sklearn.preprocessing import MinMaxScaler

from context import Context
from services.sounds_storage import SoundsStorage


def transform(ctx: Context) -> None:
    transformer = Transformer(ctx)

    transformer.drop()
    transformer.fit_transform()
    transformer.save()


class Transformer:
    def __init__(self, ctx: Context) -> None:
        self.config = ctx.config
        self.dataset = SoundsStorage(ctx).get_tracks()
        self.scaler = MinMaxScaler()

    def fit_transform(self) -> None:
        self.dataset[:] = self.scaler.fit_transform(self.dataset.values)

    def drop(self) -> None:
        self.dataset = self.dataset.drop(["name", "album", "artists"], axis=1)
        self.dataset.set_index("id", inplace=True)

    def save(self) -> Result[None, str]:
        joblib.dump(self.scaler, self.config.scaler_storage_path)
        self.dataset.to_csv(self.config.transformed_sounds_storage_path)

        compression = zipfile.ZIP_DEFLATED
        archive = zipfile.ZipFile(self.config.archive_storage_path, mode="w")
        try:
            archive.write(self.config.scaler_storage_path, compress_type=compression)
            archive.write(
                self.config.transformed_sounds_storage_path, compress_type=compression
            )
        except:
            return Err("Error while archiving")

        archive.close()

        return Ok(None)
